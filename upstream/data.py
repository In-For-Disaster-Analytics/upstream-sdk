"""
Data handling and upload functionality for Upstream SDK.
"""

import csv
import json
from typing import Dict, Any, List, Optional, Union, Iterator
from pathlib import Path
import logging

import requests
import pandas as pd

from .exceptions import ValidationError, UploadError, APIError
from .utils import ConfigManager, validate_file_size, chunk_file

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Validates data formats for Upstream API.
    """
    
    REQUIRED_SENSOR_FIELDS = ['alias', 'variablename', 'units']
    REQUIRED_MEASUREMENT_FIELDS = ['collectiontime', 'Lat_deg', 'Lon_deg']
    
    def __init__(self, config: ConfigManager) -> None:
        """
        Initialize data validator.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
    
    def validate_sensors_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate sensors data format.
        
        Args:
            data: List of sensor dictionaries
            
        Returns:
            Validation result dictionary
            
        Raises:
            ValidationError: If data format is invalid
        """
        errors = []
        
        for i, sensor in enumerate(data):
            # Check required fields
            for field in self.REQUIRED_SENSOR_FIELDS:
                if field not in sensor or not sensor[field]:
                    errors.append(f"Row {i+1}: Missing required field '{field}'")
            
            # Validate alias format
            if 'alias' in sensor and not isinstance(sensor['alias'], str):
                errors.append(f"Row {i+1}: 'alias' must be a string")
            
            # Validate units
            if 'units' in sensor and not isinstance(sensor['units'], str):
                errors.append(f"Row {i+1}: 'units' must be a string")
        
        if errors:
            raise ValidationError(f"Sensor data validation failed: {'; '.join(errors)}")
        
        return {
            'valid': True,
            'sensor_count': len(data),
            'message': f'Validated {len(data)} sensors'
        }
    
    def validate_measurements_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate measurements data format.
        
        Args:
            data: List of measurement dictionaries
            
        Returns:
            Validation result dictionary
            
        Raises:
            ValidationError: If data format is invalid
        """
        errors = []
        
        for i, measurement in enumerate(data):
            # Check required fields
            for field in self.REQUIRED_MEASUREMENT_FIELDS:
                if field not in measurement:
                    errors.append(f"Row {i+1}: Missing required field '{field}'")
            
            # Validate coordinates
            if 'Lat_deg' in measurement:
                try:
                    lat = float(measurement['Lat_deg'])
                    if not (-90 <= lat <= 90):
                        errors.append(f"Row {i+1}: Latitude must be between -90 and 90")
                except (ValueError, TypeError):
                    errors.append(f"Row {i+1}: Invalid latitude value")
            
            if 'Lon_deg' in measurement:
                try:
                    lon = float(measurement['Lon_deg'])
                    if not (-180 <= lon <= 180):
                        errors.append(f"Row {i+1}: Longitude must be between -180 and 180")
                except (ValueError, TypeError):
                    errors.append(f"Row {i+1}: Invalid longitude value")
            
            # Validate timestamp format
            if 'collectiontime' in measurement:
                timestamp = measurement['collectiontime']
                if not isinstance(timestamp, str):
                    errors.append(f"Row {i+1}: 'collectiontime' must be a string")
                # Additional timestamp format validation could be added here
        
        if errors:
            raise ValidationError(f"Measurement data validation failed: {'; '.join(errors)}")
        
        return {
            'valid': True,
            'measurement_count': len(data),
            'message': f'Validated {len(data)} measurements'
        }
    
    def validate_csv_file(self, file_path: Union[str, Path], 
                         file_type: str = 'measurements') -> Dict[str, Any]:
        """
        Validate CSV file format.
        
        Args:
            file_path: Path to CSV file
            file_type: Type of file ('sensors' or 'measurements')
            
        Returns:
            Validation result dictionary
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ValidationError(f"File not found: {file_path}")
        
        if not validate_file_size(file_path, self.config.max_chunk_size_mb):
            raise ValidationError(f"File size exceeds maximum limit: {self.config.max_chunk_size_mb}MB")
        
        try:
            # Read CSV file
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            # Validate based on file type
            if file_type == 'sensors':
                return self.validate_sensors_data(data)
            elif file_type == 'measurements':
                return self.validate_measurements_data(data)
            else:
                raise ValidationError(f"Unknown file type: {file_type}")
                
        except Exception as e:
            raise ValidationError(f"Failed to validate CSV file: {e}")


class DataUploader:
    """
    Handles data upload operations for Upstream API.
    """
    
    def __init__(self, auth_manager) -> None:
        """
        Initialize data uploader.
        
        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager
        self.base_url = auth_manager.config.base_url
        self.validator = DataValidator(auth_manager.config)
    
    def upload_csv_data(self, 
                       campaign_id: str,
                       station_id: str,
                       sensors_file: Union[str, Path],
                       measurements_file: Union[str, Path],
                       validate_data: bool = True,
                       **kwargs) -> Dict[str, Any]:
        """
        Upload sensor data from CSV files.
        
        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file
            validate_data: Whether to validate data before upload
            **kwargs: Additional upload parameters
            
        Returns:
            Upload result dictionary
        """
        sensors_file = Path(sensors_file)
        measurements_file = Path(measurements_file)
        
        # Validate files exist
        if not sensors_file.exists():
            raise ValidationError(f"Sensors file not found: {sensors_file}")
        if not measurements_file.exists():
            raise ValidationError(f"Measurements file not found: {measurements_file}")
        
        # Validate data format if requested
        if validate_data:
            logger.info("Validating sensor data format...")
            self.validator.validate_csv_file(sensors_file, 'sensors')
            
            logger.info("Validating measurement data format...")
            self.validator.validate_csv_file(measurements_file, 'measurements')
        
        # Upload files
        try:
            # First upload sensors
            sensors_result = self._upload_file(
                campaign_id=campaign_id,
                station_id=station_id,
                file_path=sensors_file,
                file_type='sensors',
                **kwargs
            )
            
            # Then upload measurements
            measurements_result = self._upload_file(
                campaign_id=campaign_id,
                station_id=station_id,
                file_path=measurements_file,
                file_type='measurements',
                **kwargs
            )
            
            return {
                'success': True,
                'sensors_result': sensors_result,
                'measurements_result': measurements_result,
                'message': 'Data uploaded successfully'
            }
            
        except Exception as e:
            logger.error(f"Data upload failed: {e}")
            raise UploadError(f"Failed to upload data: {e}")
    
    def upload_measurements(self, 
                          campaign_id: str,
                          station_id: str,
                          data: List[Dict[str, Any]],
                          validate_data: bool = True,
                          **kwargs) -> Dict[str, Any]:
        """
        Upload measurement data directly.
        
        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            data: List of measurement dictionaries
            validate_data: Whether to validate data before upload
            **kwargs: Additional upload parameters
            
        Returns:
            Upload result dictionary
        """
        if validate_data:
            logger.info("Validating measurement data...")
            self.validator.validate_measurements_data(data)
        
        try:
            # Prepare payload
            payload = {
                'campaign_id': campaign_id,
                'station_id': station_id,
                'measurements': data,
                **kwargs
            }
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/measurements",
                json=payload,
                headers=self.auth_manager.get_headers(),
                timeout=self.auth_manager.config.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            logger.info(f"Successfully uploaded {len(data)} measurements")
            return {
                'success': True,
                'upload_id': result.get('upload_id'),
                'measurements_processed': len(data),
                'message': 'Measurements uploaded successfully'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Measurement upload failed: {e}")
            raise UploadError(f"Failed to upload measurements: {e}")
    
    def _upload_file(self, 
                    campaign_id: str,
                    station_id: str,
                    file_path: Path,
                    file_type: str,
                    **kwargs) -> Dict[str, Any]:
        """
        Upload a single file to the API.
        
        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            file_path: Path to file
            file_type: Type of file ('sensors' or 'measurements')
            **kwargs: Additional parameters
            
        Returns:
            Upload result dictionary
        """
        # Check if file needs to be chunked
        if not validate_file_size(file_path, self.auth_manager.config.max_chunk_size_mb):
            return self._upload_chunked_file(campaign_id, station_id, file_path, file_type, **kwargs)
        
        # Upload single file
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'text/csv')}
                data = {
                    'campaign_id': campaign_id,
                    'station_id': station_id,
                    'file_type': file_type,
                    **kwargs
                }
                
                response = requests.post(
                    f"{self.base_url}/upload",
                    files=files,
                    data=data,
                    headers=self.auth_manager.get_headers(),
                    timeout=self.auth_manager.config.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                
                logger.info(f"Successfully uploaded {file_type} file: {file_path.name}")
                return result
                
        except Exception as e:
            raise UploadError(f"Failed to upload {file_type} file: {e}")
    
    def _upload_chunked_file(self, 
                           campaign_id: str,
                           station_id: str,
                           file_path: Path,
                           file_type: str,
                           **kwargs) -> Dict[str, Any]:
        """
        Upload large file in chunks.
        
        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            file_path: Path to file
            file_type: Type of file
            **kwargs: Additional parameters
            
        Returns:
            Upload result dictionary
        """
        logger.info(f"Chunking large file: {file_path.name}")
        
        # Split file into chunks
        chunk_files = chunk_file(
            file_path,
            chunk_size=self.auth_manager.config.chunk_size,
            max_chunk_size_mb=self.auth_manager.config.max_chunk_size_mb
        )
        
        upload_results = []
        
        try:
            for chunk_file_path in chunk_files:
                chunk_result = self._upload_file(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    file_path=Path(chunk_file_path),
                    file_type=file_type,
                    **kwargs
                )
                upload_results.append(chunk_result)
            
            return {
                'success': True,
                'chunks_uploaded': len(upload_results),
                'chunk_results': upload_results,
                'message': f'Successfully uploaded {len(upload_results)} chunks'
            }
            
        finally:
            # Clean up temporary chunk files
            for chunk_file_path in chunk_files:
                try:
                    Path(chunk_file_path).unlink()
                except Exception as e:
                    logger.warning(f"Failed to delete chunk file {chunk_file_path}: {e}")
    
    def get_upload_status(self, upload_id: str) -> Dict[str, Any]:
        """
        Get status of a data upload.
        
        Args:
            upload_id: Upload ID
            
        Returns:
            Upload status dictionary
        """
        try:
            response = requests.get(
                f"{self.base_url}/uploads/{upload_id}",
                headers=self.auth_manager.get_headers(),
                timeout=self.auth_manager.config.timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to get upload status: {e}")
    
    def list_uploads(self, campaign_id: Optional[str] = None, 
                    station_id: Optional[str] = None,
                    limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List data uploads.
        
        Args:
            campaign_id: Filter by campaign ID
            station_id: Filter by station ID
            limit: Maximum number of uploads to return
            offset: Number of uploads to skip
            
        Returns:
            List of upload dictionaries
        """
        params = {'limit': limit, 'offset': offset}
        
        if campaign_id:
            params['campaign_id'] = campaign_id
        if station_id:
            params['station_id'] = station_id
        
        try:
            response = requests.get(
                f"{self.base_url}/uploads",
                params=params,
                headers=self.auth_manager.get_headers(),
                timeout=self.auth_manager.config.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('uploads', [])
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to list uploads: {e}")