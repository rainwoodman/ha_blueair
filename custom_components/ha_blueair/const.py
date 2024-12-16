# Configuration Constants
DOMAIN: str = "ha_blueair"

# Integration Setting Constants
CONFIG_FLOW_VERSION: int = 2
PLATFORMS = ["binary_sensor", "fan", "sensor", "light", "switch"]

# Home Assistant Data Storage Constants
DATA_DEVICES: str = "api_devices"
DATA_AWS_DEVICES: str = "api_aws_devices"

REGION_EU = "eu"
REGION_USA = "us"
REGIONS = [REGION_USA, REGION_EU]

DEFAULT_FAN_SPEED_PERCENTAGE = 50
FILTER_EXPIRED_THRESHOLD = 95

# Wait time to account for latency in Blueair server side state update.
DEVICE_REFRESH_WAIT_SECONDS = 5
