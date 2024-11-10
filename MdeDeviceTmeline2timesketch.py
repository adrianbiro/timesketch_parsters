import csv
import json
from datetime import datetime

MDE_TIMELINE_CSV = "MDE03_2024-11-10.csv"
TIMESKETCH_JSONL = f"Sketch_{MDE_TIMELINE_CSV.replace(".csv", ".jsonl")}"
type timesketch_object = list[dict[str, str]]


def parse_mde_csv(path: str) -> timesketch_object:
    """
    security.microsoft.com > Assets > Devices > [Device Name] > Timeline
    https://learn.microsoft.com/en-us/defender-endpoint/device-timeline-event-flag
    Mandatory fields:
    message String with an informative message of the event
    datetime ISO8601 format for example: 2015-07-24T19:01:01+00:00
    timestamp_desc String explaining what type of timestamp it is for example file created
    """
    with open(path, "r", encoding="utf-8-sig") as csv_file:
        dict_csv = csv.DictReader(csv_file, delimiter=",")
        out_vals: timesketch_object = []
        for r in dict_csv:
            
        #return [
            d = {
                "message": r["Action Type"],
                "datetime": f"{datetime.strptime(r["Event Time"], "%Y-%m-%dT%H:%M:%S.%f").isoformat()}+00:00", # 2024-11-05T15:19:40.621
                "timestamp": datetime.strptime(r["Event Time"], "%Y-%m-%dT%H:%M:%S.%f").strftime(
                    "%s"
                ),  # unix
                "timestamp_desc": r["File Name"],
            }
            del r["Action Type"]
            del r["Event Time"]
            del r["File Name"]
            out_vals.append(d | r)
            #Event Time,Machine Id,Computer Name,Action Type,File Name,Folder Path,Sha1,Sha256,MD5,Process Command Line,Account Domain,Account Name,Account Sid,Logon Id,Process Id,Process Creation Time,Process Token Elevation,Registry Key,Registry Value Name,Registry Value Data,Remote Url,Remote Computer Name,Remote IP,Remote Port,Local IP,Local Port,File Origin Url,File Origin IP,Initiating Process SHA1,Initiating Process SHA256,Initiating Process File Name,Initiating Process Folder Path,Initiating Process Id,Initiating Process Command Line,Initiating Process Creation Time,Initiating Process Integrity Level,Initiating Process Token Elevation,Initiating Process Parent Id,Initiating Process Parent File Name,Initiating Process Parent Creation Time,Initiating Process MD5,Initiating Process Account Domain,Initiating Process Account Name,Initiating Process Account Sid,Initiating Process Logon Id,Report Id,Additional Fields,App Guard Container Id,Protocol,Logon Type,Process Integrity Level,Registry Value Type,Previous Registry Value Name,Previous Registry Value Data,Previous Registry Key,File Origin Referrer Url,Sensitivity Label,Sensitivity Sub Label,Is Endpoint Dlp Applied,Is Azure Info Protection Applied,Alert Ids,Categories,Severities,Is Marked,Data Type
    return out_vals


def create_jsonl(data: timesketch_object) -> None:
    """
    Create jsonl file
    https://timesketch.org/guides/user/import-from-json-csv/
    """
    with open(
        TIMESKETCH_JSONL, "w", encoding="utf-8"
    ) as f:  # timesketch requred encoding is without bom
        for l in data:
            f.write(f"{json.dumps(l,ensure_ascii=False)}\n")


def main() -> None:
    """main logic"""
    tso: timesketch_object = parse_mde_csv(MDE_TIMELINE_CSV)
    create_jsonl(tso)


if __name__ == "__main__":
    raise SystemExit(main())
