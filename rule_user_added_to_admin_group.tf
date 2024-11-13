module "user_added_to_admin_group" {
    source   = "C:\\Users\\camhu\\DaC\\modules\\splunk_saved_searches"
    auth_token = var.SPLUNK_AUTH_TOKEN    
    name = "User Added to Admin Group"
    search = "index=* host=\"AR-WINDC2019\" EventID=\"5136\" | spath input=_raw path=\"Event.System.TimeCreated{@SystemTime}\" output=TimeCreated | spath input=_raw path=Event.EventData.Data{9} output=GUID | spath input=_raw path=Event.System.Computer output=InitiatingDevice | spath input=_raw path=Event.EventData.Data{4} output=InitiatingUser | rex field=AttributeValue \"cn=(?<Username>[^,]+)\" | rex field=GUID \"CN=(?<GroupMembership>[^,]+)\" | rename name as EventDescription | where like(GUID, \"%Admin%\") | table TimeCreated, InitiatingUser, InitiatingDevice, EventDescription, Username, GroupMembership, AttributeValue, GUID"
    cron_schedule = "*/5 * * * *"
    alert = true
    is_scheduled = true
}