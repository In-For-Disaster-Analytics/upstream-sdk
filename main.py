import os
from upstream import UpstreamClient

# Initialize client
client = UpstreamClient(
    username=os.getenv("UPSTREAM_USERNAME"),
    password=os.getenv("UPSTREAM_PASSWORD"),
    base_url=os.getenv("UPSTREAM_BASE_URL"),
)
# Create campaign and station
campaigns = client.list_campaigns()
print(campaigns.items[0].id)

for campaign in campaigns.items:
    print(campaign.id)
    print(campaign.name)
    print(campaign.start_date)
    print(campaign.end_date)
    print(campaign.allocation)
