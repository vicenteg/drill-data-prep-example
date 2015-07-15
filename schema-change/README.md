# Scenario

You have data where the schema changes. In this example, we look at the case where you have a field that changes from a single value to a list, or vice versa.

# Sample Data

This data is split across two files.

```json
{
  "name": "Vince",
  "favorite_foods": [
    {
      "name": "ice-cream",
      "flavors": "vanilla"
    },
    {
      "name": "cheeseburgers",
      "flavors": [
        "animal style",
        "black label"
      ]
    }
  ]
}
```

```json
{
  "name": "Nikki",
  "favorite_foods": [
    {
      "name": "ice-cream",
      "flavors": [
        "chocolate",
        "dulce de leche"
      ]
    },
    {
      "name": "cheeseburgers",
      "flavors": [
        "black label"
      ]
    }
  ]
}
```

# Query

Both files are valid JSON, and that's good, but it turns out that the schema changes. Vince only like vanilla ice cream, and that's stored as a single value. Nikki likes chocolate and dulce de leche (Vince won't turn those down, just not his favorite) so those are stored as a list. 

Drill would rather you not organize your data this way, and is not shy about telling you so:

```
0: jdbc:drill:zk=local> select * from `/Users/vince/src/mapr/drill-data-prep/schema-change/data`;
java.lang.RuntimeException: java.sql.SQLException: DATA_READ ERROR: You tried to start when you are using a ValueWriter of type NullableVarCharWriterImpl.

File  /Users/vince/src/mapr/drill-data-prep/schema-change/data/vince.json
Record  1
Line  1
Column  127
Field  flavors
Fragment 0:0

[Error Id: 2c9020c1-cfcf-42e2-926c-d00962ceb7f9 on 192.168.56.1:31010]
	at sqlline.IncrementalRows.hasNext(IncrementalRows.java:73)
	at sqlline.TableOutputFormat$ResizingRowsProvider.next(TableOutputFormat.java:87)
	at sqlline.TableOutputFormat.print(TableOutputFormat.java:118)
	at sqlline.SqlLine.print(SqlLine.java:1583)
	at sqlline.Commands.execute(Commands.java:852)
	at sqlline.Commands.sql(Commands.java:751)
	at sqlline.SqlLine.dispatch(SqlLine.java:738)
	at sqlline.SqlLine.begin(SqlLine.java:612)
	at sqlline.SqlLine.start(SqlLine.java:366)
	at sqlline.SqlLine.main(SqlLine.java:259)
```

What if we reverse the order of these objects in the input? Does Drill like it better when we start it off with a list, then change to a single value?

```
0: jdbc:drill:zk=local> select * from `/Users/vince/src/mapr/drill-data-prep/schema-change/data`;
Error: DATA_READ ERROR: You tried to write a VarChar type when you are using a ValueWriter of type SingleListWriter.

File  /Users/vince/src/mapr/drill-data-prep/schema-change/sample_data.json
Record  2
Line  3
Column  84
Field  flavors
Fragment 0:0

[Error Id: 93ceda84-8710-46de-8d5f-6b2290914703 on 192.168.56.1:31010] (state=,code=0)
```

No. Drill is still displeased.

# What's the problem?

Drill doesn't like it when you give it data where the type changes from something like a single value to a list, or vice versa. 

# How do we work around it?

We massage the data so that fields where lists are sometimes, but not always, used become fields where lists are always used. In the sample data, one of the `flavors` fields was the issue. Drill helpfully pinpointed the line and the column that it had an issue with, so you can eyeball it before you go and start writing code to fix it.

One way to fix the data is in python. You can simply read in the JSON objects and rewrite them converting single values into single-value lists:

```python
import json
import types

for filename in ("data/vince.json", "data/nikki.json"):
	# Read the file into memory.
	with file(filename) as infile:
		data = json.loads(infile.read())

	# Open and truncate the input file.
	with file(filename, "w") as outfile:
		# enumerate returns an incrementing integer with each iteration.
		# convenient way to keep track of the index into the list
		# we need to modify.
		for i,f in enumerate(data["favorite_foods"]):
			# Check if the value pointed to by "flavors" is of type
			# ListType.
		    if type(f["flavors"]) != types.ListType:
		    	# If it's not, then overwrite the value as a list.
				data["favorite_foods"][i]["flavors"] = [ f["flavors"] ]
		outfile.write(json.dumps(data))
```

Now, querying the massaged data, Drill is happier:

```
0: jdbc:drill:zk=local> select * from `/Users/vince/src/mapr/drill-data-prep/schema-change/data`;
+---------------------------------------------------------------------------------------------------------------------+--------+
|                                                   favorite_foods                                                    |  name  |
+---------------------------------------------------------------------------------------------------------------------+--------+
| [{"flavors":["chocolate","dulce de leche"],"name":"ice-cream"},{"flavors":["black label"],"name":"cheeseburgers"}]  | Nikki  |
| [{"flavors":["vanilla"],"name":"ice-cream"},{"flavors":["animal style","black label"],"name":"cheeseburgers"}]      | Vince  |
+---------------------------------------------------------------------------------------------------------------------+--------+
2 rows selected (0.119 seconds)
```

More happy queries:

```
0: jdbc:drill:zk=local> select t.name, t.yum.name as fave_food, flatten(t.yum.flavors) as fave_flave from (select t.name, flatten(t.favorite_foods) as yum from (select name,favorite_foods from `/Users/vince/src/mapr/drill-data-prep/schema-change/data`) t) t;
+--------+----------------+-----------------+
|  name  |   fave_food    |   fave_flave    |
+--------+----------------+-----------------+
| Nikki  | ice-cream      | chocolate       |
| Nikki  | ice-cream      | dulce de leche  |
| Nikki  | cheeseburgers  | black label     |
| Vince  | ice-cream      | vanilla         |
| Vince  | cheeseburgers  | animal style    |
| Vince  | cheeseburgers  | black label     |
+--------+----------------+-----------------+
6 rows selected (0.153 seconds)
```


# Interesting(?) note

You get different style of error output when you query a directory of JSON files than when you query a file.

