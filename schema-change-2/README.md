# Scenario

You have data where the schema changes. In this case, the value of a nested part of the data changes from an empty list to a non-empty list.


# Sample Data

This data is split across two files, partitioned by date.

```json
{
    "data": [],
    "status": "OK",
    "timeofday": "2015-05-14 05:32:16.022 GMT+0000",
    "timestamp": 1431624736022,
    "total": 0
}
```

```json
{
    "data": [
        {
            "alarm name": "NODE_ALARM_SERVICE_NFS_DOWN",
            "alarm state": 1,
            "alarm statechange time": 1433439779492,
            "description": "Can not determine if service: nfs is running. Check logs at: /opt/mapr/logs/nfsserver.log",
            "entity": "node1"
        },
        {
            "alarm name": "NODE_ALARM_SERVICE_NFS_DOWN",
            "alarm state": 1,
            "alarm statechange time": 1433431833317,
            "description": "Can not determine if service: nfs is running. Check logs at: /opt/mapr/logs/nfsserver.log",
            "entity": "node4"
        },
        {
            "alarm name": "NODE_ALARM_SERVICE_NFS_DOWN",
            "alarm state": 1,
            "alarm statechange time": 1433439067671,
            "description": "Can not determine if service: nfs is running. Check logs at: /opt/mapr/logs/nfsserver.log",
            "entity": "node3"
        },
        {
            "alarm name": "NODE_ALARM_SERVICE_CLDB_DOWN",
            "alarm state": 1,
            "alarm statechange time": 1433440037100,
            "description": "Can not determine if service: cldb is running. Check logs at: /opt/mapr/logs/cldb.log",
            "entity": "node2"
        }
    ],
    "status": "OK",
    "timeofday": "2015-06-04 01:57:31.404 GMT-0400",
    "timestamp": 1433440651404,
    "total": 4
}
```

# Query


I can select data:

```
0: jdbc:drill:zk=local> select dir1,data from `/Users/vince/src/mapr/drill-data-prep/schema-change-2/data/maprcli_alarm_list/`;
+------+------+
| dir1 | data |
+------+------+
| se1 | null |
| cluster.vincegonzalez.net | [{"alarm name":"NODE_ALARM_SERVICE_NFS_DOWN","alarm state":1,"alarm statechange time":1433439779492,"description":"Can not determine if service: nfs is running. Check logs at: /opt/mapr/logs/nfsserver.log","entity":"node1"},{"alarm name":"NODE_ALARM_SERVICE_NFS_DOWN","alarm state":1,"alarm statechange time":1433431833317,"description":"Can not determine if service: nfs is running. Check logs at: /opt/mapr/logs/nfsserver.log","entity":"node4"},{"alarm name":"NODE_ALARM_SERVICE_NFS_DOWN","alarm state":1,"alarm statechange time":1433439067671,"description":"Can not determine if service: nfs is running. Check logs at: /opt/mapr/logs/nfsserver.log","entity":"node3"},{"alarm name":"NODE_ALARM_SERVICE_CLDB_DOWN","alarm state":1,"alarm statechange time":1433440037100,"description":"Can not determine if service: cldb is running. Check logs at: /opt/mapr/logs/cldb.log","entity":"node2"}] |
+------+------+
2 rows selected (0.116 seconds)
```

But I can't flatten the list because we go from a the `data` key changing from an empty list (which Drill turns into a null) to a vector:

```
0: jdbc:drill:zk=local> select dir1,flatten(data) from `/Users/vince/src/mapr/drill-data-prep/schema-change-2/data/maprcli_alarm_list/`;
Error: SYSTEM ERROR: ClassCastException: Cannot cast org.apache.drill.exec.vector.NullableIntVector to org.apache.drill.exec.vector.complex.RepeatedValueVector

Fragment 0:0

[Error Id: e6b86be5-b5b8-4af5-ac95-198c55ba7da8 on 172.16.0.236:31010] (state=,code=0)
```

# What's the problem?

```
¯\_(ツ)_/¯
```

# How do we work around it?

```
¯\_(ツ)_/¯
```
