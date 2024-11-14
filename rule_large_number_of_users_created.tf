module "test" {
    source   = "C:\\Users\\camhu\\DaC\\modules\\splunk_saved_searches"
    auth_token = var.SPLUNK_AUTH_TOKEN    
    name = "Large Number of Users Added to AD Environment"
    search = "index=ActiveDirectory host=\"AR-WINDC2019\" source=\"xmlwineventlog:security\" name=\"A user account was enabled\" | spath input=_raw path=Event.System.Computer output=InitiatingDevice | spath input=_raw path=Event.System.EventID output=EventID | spath input=_raw path=Event.EventData.Data{1} output=TargetUserName | where NOT match(TargetUserName, \"\\$$\") | spath input=_raw path=Event.EventData.Data{5} output=InitiatingUserName | spath input=_raw path=Event.System.Provider output=name | table source, InitiatingDevice, EventID, InitiatingUserName, TargetUserName"
    cron_schedule = "*/5 * * * *"
    alert = true
    is_scheduled = true
}