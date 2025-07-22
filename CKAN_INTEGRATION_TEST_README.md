# CKAN Integration Test Setup

## Overview

The CKAN integration test `test_ckan_dataset_update_integration()` verifies that the enhanced `update_dataset` functionality works correctly with a real CKAN instance.

## Error Resolution

### Organization Required Error
If you see the error:
```
"{'owner_org': ['An organization must be provided'], '__type': 'Validation Error'}"
```

This means the CKAN instance requires datasets to be created under an organization. The test has been updated to handle this requirement by:
- Adding `organization=ORGANIZATION` parameter to dataset creation
- Adding validation to ensure `CKAN_ORGANIZATION` environment variable is set
- Skipping the test if organization is not configured

### Tag Order Assertion Error  
If you see an assertion error like:
```
AssertionError: assert ['final', 'replaced'] == ['replaced', 'final']
```

This is because CKAN doesn't guarantee tag order. The test has been updated to use order-independent comparison:
- Uses `set()` comparison for tag validation
- Validates tag count separately to ensure no missing/extra tags
- Focuses on content validation rather than order

## Required Environment Variables

Set the following environment variables before running the integration test:

```bash
# Upstream API credentials
export UPSTREAM_USERNAME=your_upstream_username
export UPSTREAM_PASSWORD=your_upstream_password

# CKAN credentials and configuration
export CKAN_API_KEY=your_ckan_api_key
export CKAN_ORGANIZATION=your_organization_name

# Optional: Override default URLs
export CKAN_URL=http://ckan.tacc.cloud:5000  # Default
export UPSTREAM_BASE_URL=http://localhost:8000  # Default
```

## How to Run the Test

### Option 1: Run the specific test
```bash
pytest tests/integration/test_campaigns_integration.py::test_ckan_dataset_update_integration -v -s
```

### Option 2: Run all integration tests
```bash
pytest tests/integration/ -m integration -v
```

## What the Test Does

The integration test performs a complete workflow:

1. **Creates** an initial CKAN dataset with:
   - Tags: `["test", "initial"]`
   - Metadata: `{"test_phase": "initial", "created_by": "integration_test"}`

2. **Updates** the dataset using merge mode:
   - Adds tags: `["updated", "integration-test"]`
   - Adds/updates metadata: `{"test_phase": "updated", "update_timestamp": "...", "integration_status": "passed"}`
   - Updates title to "Updated Test Dataset"

3. **Verifies** merge results:
   - Both old and new tags present: `["test", "initial", "updated", "integration-test"]`
   - Both old and new metadata present
   - Updated fields have new values
   - Preserved fields remain unchanged

4. **Tests** replace mode:
   - Replaces all tags with: `["replaced", "final"]`
   - Replaces all metadata with: `{"final_phase": "replace_test", "mode": "replace"}`

5. **Verifies** replace results:
   - Only new tags present (old ones removed)
   - Only new metadata present (old ones removed)

6. **Cleans up** by deleting the test dataset

## Expected Output

```
Testing CKAN dataset update integration with: test-dataset-update-20250722211732
✅ Created initial dataset: test-dataset-update-20250722211732
✅ Verified initial dataset state
🔄 Updating dataset with new tag and metadata...
✅ Updated dataset: test-dataset-update-20250722211732
🔍 Verifying updates...
  ✓ Title updated successfully
  ✓ Tags updated successfully: ['test', 'initial', 'updated', 'integration-test']
  ✓ Original metadata preserved
  ✓ Existing metadata updated
  ✓ New metadata added
✅ All updates verified successfully!
🔄 Testing replace mode...
  ✓ Tags replaced successfully
  ✓ Metadata replaced successfully
✅ Replace mode test passed!
🧹 Cleaned up test dataset: test-dataset-update-20250722211732
🎉 CKAN dataset update integration test completed successfully!
```

## Troubleshooting

### No Organization Access
If you get organization errors, ask your CKAN admin to:
1. Create an organization for testing
2. Add your user to the organization with editor/admin permissions

### API Key Issues
- Ensure your CKAN API key has permissions to create/update/delete datasets
- Check that the API key hasn't expired
- Verify the API key format matches your CKAN instance requirements

### Network Issues
- Ensure the CKAN URL is accessible from your testing environment
- Check firewall and network connectivity
- Verify the CKAN instance is running and responding

## Files Modified

- `tests/integration/test_campaigns_integration.py` - Added comprehensive integration test
- `upstream/ckan.py` - Enhanced `update_dataset` method with metadata support
- `tests/unit/test_ckan_unit.py` - Added unit tests for enhanced functionality