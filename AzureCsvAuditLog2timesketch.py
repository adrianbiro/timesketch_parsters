import csv
import json
from datetime import datetime

CSV_AZURE_AUDIT = "AuditLogs_2024-11-09.csv"
TIMESKETCH_JSONL = f"Sketch_{CSV_AZURE_AUDIT.replace(".csv", ".jsonl")}"
type timesketch_object = list[dict[str, str]]


def parse_csv_azure_audit_log(path: str) -> timesketch_object:
    """
    Parse manually exported CSV Audit Log
    Mandatory fields:
    message String with an informative message of the event
    datetime ISO8601 format for example: 2015-07-24T19:01:01+00:00
    timestamp_desc String explaining what type of timestamp it is for example file created
    """
    with open(path, "r", encoding="utf-8-sig") as csv_file:
        dict_csv = csv.DictReader(csv_file, delimiter=",")
        return [
            {
                "message": r["Category"],
                "datetime": r["Date (UTC)"],  # 2015-07-24T19:01:01+00:00
                "timestamp": datetime.fromisoformat(r["Date (UTC)"]).strftime(
                    "%s"
                ),  # unix
                "timestamp_desc": r["Activity"],
                "ActorType": r["ActorType"],
                "ActorUserPrincipalName": r["ActorUserPrincipalName"],
                "IPAddress": r["IPAddress"],
                "Service": r["Service"],
                "ResultReason": r["ResultReason"],
                "Result": r["Result"],
                "ActionModificationDetails": f"{r["Target1ModifiedProperty1Name"]}: {r['Target1ModifiedProperty1NewValue']}",
                # "Date (UTC)","CorrelationId","Service","Category","Activity","Result","ResultReason","User Agent","ActorType","ActorDisplayName","ActorObjectId","ActorUserPrincipalName","IPAddress","ActorHomeTenantId","ActorHomeTenantName","ActorServicePrincipalId","ActorServicePrincipalName","Target1Type","Target1DisplayName","Target1ObjectId","Target1UserPrincipalName","Target1ModifiedProperty1Name","Target1ModifiedProperty1OldValue","Target1ModifiedProperty1NewValue","Target1ModifiedProperty2Name","Target1ModifiedProperty2OldValue","Target1ModifiedProperty2NewValue","Target1ModifiedProperty3Name","Target1ModifiedProperty3OldValue","Target1ModifiedProperty3NewValue","Target1ModifiedProperty4Name","Target1ModifiedProperty4OldValue","Target1ModifiedProperty4NewValue","Target1ModifiedProperty5Name","Target1ModifiedProperty5OldValue","Target1ModifiedProperty5NewValue","Target2Type","Target2DisplayName","Target2ObjectId","Target2UserPrincipalName","Target2ModifiedProperty1Name","Target2ModifiedProperty1OldValue","Target2ModifiedProperty1NewValue","Target2ModifiedProperty2Name","Target2ModifiedProperty2OldValue","Target2ModifiedProperty2NewValue","Target2ModifiedProperty3Name","Target2ModifiedProperty3OldValue","Target2ModifiedProperty3NewValue","Target2ModifiedProperty4Name","Target2ModifiedProperty4OldValue","Target2ModifiedProperty4NewValue","Target2ModifiedProperty5Name","Target2ModifiedProperty5OldValue","Target2ModifiedProperty5NewValue","Target3Type","Target3DisplayName","Target3ObjectId","Target3UserPrincipalName","Target3ModifiedProperty1Name","Target3ModifiedProperty1OldValue","Target3ModifiedProperty1NewValue","Target3ModifiedProperty2Name","Target3ModifiedProperty2OldValue","Target3ModifiedProperty2NewValue","Target3ModifiedProperty3Name","Target3ModifiedProperty3OldValue","Target3ModifiedProperty3NewValue","Target3ModifiedProperty4Name","Target3ModifiedProperty4OldValue","Target3ModifiedProperty4NewValue","Target3ModifiedProperty5Name","Target3ModifiedProperty5OldValue","Target3ModifiedProperty5NewValue","AdditionalDetail1Key","AdditionalDetail1Value","AdditionalDetail2Key","AdditionalDetail2Value","AdditionalDetail3Key","AdditionalDetail3Value","AdditionalDetail4Key","AdditionalDetail4Value","AdditionalDetail5Key","AdditionalDetail5Value","AdditionalDetail6Key","AdditionalDetail6Value"
            }
            for r in dict_csv
        ]


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
    tso: timesketch_object = parse_csv_azure_audit_log(CSV_AZURE_AUDIT)
    create_jsonl(tso)


if __name__ == "__main__":
    raise SystemExit(main())
