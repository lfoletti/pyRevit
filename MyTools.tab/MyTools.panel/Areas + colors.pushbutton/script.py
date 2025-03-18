from pyrevit import revit, DB

# Get the active document
doc = revit.doc
t = DB.Transaction(doc, "Create Zone Area Schedule")
t.Start()

# Check if the schedule already exists
existing_schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
schedule_name = "Zone Area Schedule"
for sched in existing_schedules:
    if sched.Name == schedule_name:
        print(f"Schedule '{schedule_name}' already exists.")
        t.RollBack()
        return

# Create a new schedule for MEP Zones
zone_schedule = DB.ViewSchedule.CreateSchedule(doc, DB.BuiltInCategory.OST_MEPZones)

# Set schedule name
zone_schedule.Name = schedule_name

# Define schedule fields
fields = [
    ("Name", DB.ScheduleFieldType.Instance),
    ("Area", DB.ScheduleFieldType.Instance)
]

# Add fields to schedule
for field_name, field_type in fields:
    param_id = None
    for binding in zone_schedule.Definition.GetSchedulableFields():
        if binding.GetName() == field_name:
            param_id = binding.ParameterId
            break
    if param_id:
        field = zone_schedule.Definition.AddField(DB.ScheduleFieldType.Instance, param_id)
        print(f"Added field: {field_name}")

# Commit transaction
t.Commit()

print(f"'{schedule_name}' created successfully!")
