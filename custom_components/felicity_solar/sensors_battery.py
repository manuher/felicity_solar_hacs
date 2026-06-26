from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
)
from homeassistant.const import (
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Base descriptions
BATTERY_DESCRIPTIONS: list[SensorEntityDescription] = [
    SensorEntityDescription(key="voltage", name="Voltage",
                            native_unit_of_measurement=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE),
    SensorEntityDescription(key="current", name="Current",
                            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE, device_class=SensorDeviceClass.CURRENT),
    SensorEntityDescription(key="soc", name="State of Charge",
                            native_unit_of_measurement=PERCENTAGE, device_class=SensorDeviceClass.BATTERY),
    SensorEntityDescription(key="soh", name="State of Health",
                            native_unit_of_measurement=PERCENTAGE),
    SensorEntityDescription(key="tempMax", name="Max Temperature",
                            native_unit_of_measurement=UnitOfTemperature.CELSIUS, device_class=SensorDeviceClass.TEMPERATURE),
    SensorEntityDescription(key="tempMin", name="Min Temperature",
                            native_unit_of_measurement=UnitOfTemperature.CELSIUS, device_class=SensorDeviceClass.TEMPERATURE),
    SensorEntityDescription(key="voltage_max", name="Max Cell Voltage",
                            native_unit_of_measurement=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE,
                            suggested_display_precision=3),
    SensorEntityDescription(key="voltage_min", name="Min Cell Voltage",
                            native_unit_of_measurement=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE,
                            suggested_display_precision=3),
    SensorEntityDescription(key="voltage_delta", name="Battery Cell Voltage Delta",
                            native_unit_of_measurement=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE,
                            suggested_display_precision=3),
]

# Dynamically add cell voltages
BATTERY_DESCRIPTIONS.extend([
    SensorEntityDescription(key=f"cell_{i}_voltage_v", name=f"Cell {i} Voltage",
                            native_unit_of_measurement=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE, suggested_display_precision=2)
    for i in range(1, 17)
])

# Dynamically add cell temperatures
BATTERY_DESCRIPTIONS.extend([
    SensorEntityDescription(key=f"cell_{i}_temp_c", name=f"Cell {i} Temperature",
                            native_unit_of_measurement=UnitOfTemperature.CELSIUS, device_class=SensorDeviceClass.TEMPERATURE)
    for i in range(1, 5)
])


def create_battery_sensors(coordinator, device_sn):
    return [FelicityBatterySensor(coordinator, device_sn, desc) for desc in BATTERY_DESCRIPTIONS]


class FelicityBatterySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_sn: str, description: SensorEntityDescription):
        super().__init__(coordinator)
        self.entity_description = description
        self.device_sn = device_sn
        self._attr_unique_id = f"{device_sn}_{description.key}"
        self._attr_device_info = {
            "identifiers": {("felicity_solar", device_sn)},
            "name": f"Felicity Battery {device_sn}",
            "manufacturer": "Felicity Solar",
            "model": "Lithium Battery Pack",
        }

    @property
    def native_value(self):
        device_data = self.coordinator.data.get(
            self.device_sn, {}).get("data", {})
        return device_data.get(self.entity_description.key)