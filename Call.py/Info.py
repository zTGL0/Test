# Get started with Axiom API

> This section explains how to send data to Axiom, query data, and manage resources using the Axiom API.

You can use the Axiom API (Application Programming Interface) to send data to Axiom, query data, and manage resources programmatically. This page covers the basics for interacting with the Axiom API.

## Prerequisites

* [Create an Axiom account](https://app.axiom.co/register).
* [Create a dataset in Axiom](/reference/datasets#create-dataset) where you send your data.

## API basics

Axiom API follows the REST architectural style and uses JSON for serialization. You can send API requests to Axiom with curl or API tools such as [Postman](https://www.postman.com/).

For example, the following curl command ingests data to an Axiom dataset:

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest' \
  -H 'Authorization: Bearer API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '[
    {
      "axiom": "logs"
    }
  ]'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

For more information, see [Send data to Axiom via API](/restapi/ingest) and [Ingest data endpoint](/restapi/endpoints/ingestIntoDataset).

## Regions

All examples in the Axiom API reference use the base domain `https://api.axiom.co`, which is the default for the US region. If your organization uses the EU region, change the base domain in the examples to `https://api.eu.axiom.co`.

For more information on regions, see [Regions](/reference/regions).

## Content type

Encode the body of API requests as JSON objects and set the `Content-Type` header to `application/json`. Unless otherwise specified, Axiom encodes all responses (including errors) as JSON objects.

## Authentication

To prove that API requests come from you, you must include forms of authentication called tokens in your API requests. Axiom offers two types of tokens:

* [API tokens](/reference/tokens#api-tokens) let you control the actions that can be performed with the token. For example, you can specify that requests authenticated with a certain API token can only query data from a particular dataset.
* [Personal access tokens (PATs)](/reference/tokens#personal-access-tokens-pat) provide full control over your Axiom account. Requests authenticated with a PAT can perform every action you can perform in Axiom. When possible, use API tokens instead of PATs.

If you use an API token for authentication, include the API token in the `Authorization` header.

```bash
Authorization: Bearer API_TOKEN
```

If you use a PAT for authentication, include the PAT in the `Authorization` header and the org ID in the `x-axiom-org-id` header. For more information, see [Determine org ID](/reference/tokens#determine-org-id).

```bash
Authorization: Bearer API_TOKEN
x-axiom-org-id: ORG_ID
```

If authentication is unsuccessful for a request, Axiom returns the error status code `403`.

## Data types

Below is a list of the types of data used within the Axiom API:

| Name        | Definition                                                        | Example                 |
| ----------- | ----------------------------------------------------------------- | ----------------------- |
| **ID**      | A unique value used to identify resources.                        | "io12h34io1h24i"        |
| **String**  | A sequence of characters used to represent text.                  | "string value"          |
| **Boolean** | A type of two possible values representing true or false.         | true                    |
| **Integer** | A number without decimals.                                        | 4567                    |
| **Float**   | A number with decimals.                                           | 15.67                   |
| **Map**     | A data structure with a list of values assigned to a unique key.  | \{ "key": "value" }     |
| **List**    | A data structure with only a list of values separated by a comma. | \["value", 4567, 45.67] |

## What’s next

* [Ingest data via API](/restapi/ingest)
* [Query data via API](/restapi/query)
# Send data to Axiom via API

> This page explains how to send to Axiom using the API.

The Axiom REST API accepts the following data formats:

* [JSON](#send-data-in-json-format)
* [NDJSON](#send-data-in-ndjson-format)
* [CSV](#send-data-in-csv-format)

This page explains how to send data to Axiom via cURL commands in each of these formats, and how to send data with the [Axiom Node.js library](#send-data-with-axiom-node-js).

For more information on other ingest options, see [Send data](send-data/methods).

For an introduction to the basics of the Axiom API and to the authentication options, see [Introduction to Axiom API](/restapi/introduction).

The API requests on this page use the ingest data endpoint. For more information, see the [API reference](/restapi/endpoints/ingestIntoDataset).

## Prerequisites

* [Create an Axiom account](https://app.axiom.co/register).
* [Create a dataset in Axiom](/reference/datasets#create-dataset) where you send your data.
* [Create an API token in Axiom](/reference/tokens) with permissions to update the dataset you have created.

## Send data in JSON format

To send data to Axiom in JSON format:

1. Encode the events as JSON objects.
2. Enter the array of JSON objects into the body of the API request.
3. Optional: In the body of the request, set optional parameters such as `timestamp-field` and `timestamp-format`. For more information, see the [ingest data API reference](/restapi/endpoints/ingestIntoDataset).
4. Set the `Content-Type` header to `application/json`.
5. Set the `Authorization` header to `Bearer API_TOKEN`.
6. Send the POST request to `https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest`.

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

### Example with grouped events

The following example request contains grouped events. The structure of the JSON payload has the scheme of `[ { "labels": { "key1": "value1", "key2": "value2" } }, ]` where the array contains one or more JSON objects describing events.

**Example request**

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest' \
  -H 'Authorization: Bearer API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '[
        {
          "time":"2025-01-12T00:00:00.000Z",
          "data":{"key1":"value1","key2":"value2"}
        },
        {
          "data":{"key3":"value3"},
          "labels":{"key4":"value4"}
        }
      ]'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

**Example response**

```json
{
    "ingested": 2,
    "failed": 0,
    "failures": [],
    "processedBytes": 219,
    "blocksCreated": 0,
    "walLength": 2
}
```

### Example with nested arrays

**Example request**

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest' \
    -H 'Authorization: Bearer API_TOKEN' \
    -H 'Content-Type: application/json' \
    -d '[
            {
            "axiom": [{
                "logging":[{
                    "observability":[{
                        "location":[{
                            "credentials":[{
                                "datasets":[{
                                    "first_name":"axiom",
                                    "last_name":"logging",
                                    "location":"global"
                                }],
                                "work":[{
                                    "details":"https://app.axiom.co/",
                                    "tutorials":"https://www.axiom.co/blog",
                                    "changelog":"https://www.axiom.co/changelog",
                                    "documentation": "https://www.axiom.co/docs"
                                }]
                            }],
                            "social_media":[{
                                "details":[{
                                    "twitter":"https://twitter.com/AxiomFM",
                                    "linkedin":"https://linkedin.com/company/axiomhq",
                                    "github":"https://github.com/axiomhq"
                                }],
                                "features":[{
                                    "datasets":"view logs",
                                    "stream":"live_tail",
                                    "explorer":"queries"
                                }]
                            }]
                        }]
                    }],
                    "logs":[{
                        "apl": "functions"
                    }]
                }],
                "storage":[{}]
            }]}
        ]'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

**Example response**

```json
{
    "ingested":1,
    "failed":0,
    "failures":[],
    "processedBytes":1587,
    "blocksCreated":0,
    "walLength":3
}
```

### Example with objects, strings, and arrays

**Example request**

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest' \
    -H 'Authorization: Bearer API_TOKEN' \
    -H 'Content-Type: application/json' \
    -d '[{ "axiom": {
        "logging": {
            "observability": [
                { "apl": 23, "function": "tostring" },
                { "apl": 24, "operator": "summarize" }
            ],
            "axiom": [
                { "stream": "livetail", "datasets": [4, 0, 16], "logging": "observability", "metrics": 8, "dashboard": 10, "alerting": "kubernetes" }
            ]
        },
        "apl": {
            "reference":
                [[80, 12], [30, 40]]
        }
    }
    }]'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

**Example response**

```json
{
    "ingested":1,
    "failed":0,
    "failures":[],
    "processedBytes":432,
    "blocksCreated":0,
    "walLength":4
}
```

## Send data in NDJSON format

To send data to Axiom in NDJSON format:

1. Encode the events as JSON objects.
2. Enter each JSON object in a separate line into the body of the API request.
3. Optional: In the body of the request, set optional parameters such as `timestamp-field` and `timestamp-format`. For more information, see the [ingest data API reference](/restapi/endpoints/ingestIntoDataset).
4. Set the `Content-Type` header to either `application/json` or `application/x-ndjson`.
5. Set the `Authorization` header to `Bearer API_TOKEN`. Replace `API_TOKEN` with the Axiom API token you have generated.
6. Send the POST request to `https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest`. Replace `DATASET_NAME` with the name of the Axiom dataset where you want to send data.

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

**Example request**

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest' \
    -H 'Authorization: Bearer API_TOKEN' \
    -H 'Content-Type: application/x-ndjson' \
    -d '{"id":1,"name":"machala"}
        {"id":2,"name":"axiom"}
        {"id":3,"name":"apl"}
        {"index": {"_index": "products"}}
        {"timestamp": "2016-06-06T12:00:00+02:00", "attributes": {"key1": "value1","key2": "value2"}}
        {"queryString": "count()"}'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

**Example response**

```json
{
    "ingested": 6,
    "failed": 0,
    "failures": [],
    "processedBytes": 266,
    "blocksCreated": 0,
    "walLength": 6
}
```

## Send data in CSV format

To send data to Axiom in JSON format:

1. Encode the events in CSV format. The first line specifies the field names separated by commas. Subsequent new lines specify the values separated by commas.
2. Enter the CSV representation in the body of the API request.
3. Optional: In the body of the request, set optional parameters such as `timestamp-field` and `timestamp-format`. For more information, see the [ingest data API reference](/restapi/endpoints/ingestIntoDataset).
4. Set the `Content-Type` header to `text/csv`.
5. Set the `Authorization` header to `Bearer API_TOKEN`. Replace `API_TOKEN` with the Axiom API token you have generated.
6. Send the POST request to `https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest`. Replace `DATASET_NAME` with the name of the Axiom dataset where you want to send data.

<Info>
  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.

  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).
</Info>

**Example request**

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/ingest' \
    -H 'Authorization: Bearer API_TOKEN' \
    -H 'Content-Type: text/csv' \
    -d 'user, name
        foo, bar'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

**Example response**

```json
{
    "ingested": 1,
    "failed": 0,
    "failures": [],
    "processedBytes": 28,
    "blocksCreated": 0,
    "walLength": 2
}
```

## Send data with Axiom Node.js

1. [Install and configure](/guides/javascript#use-axiomhq-js) the Axiom Node.js library.
2. Encode the events as JSON objects.
3. Pass the dataset name and the array of JSON objects to the `axiom.ingest` function.

   ```ts
   axiom.ingest('DATASET_NAME', [{ foo: 'bar' }]);
   await axiom.flush();
   ```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

For more information on other libraries you can use to query data, see [Send data](send-data/methods).

## What’s next

After ingesting data to Axiom, you can [query it via API](/restapi/query) or the [Axiom app UI](/query-data/explore).
# Query data via Axiom API

> Learn how to use the Axiom API to query data.

This page explains how to query data via the Axiom API using the following:

* [cURL](#query-data-with-curl)
* [Axiom Node.js library](#query-data-with-axiom-nodejs)

For an introduction to the basics of the Axiom API and to the authentication options, see [Introduction to Axiom API](/restapi/introduction).

The API requests on this page use the query data endpoint. For more information, see the [API reference](/restapi/endpoints/queryApl).

## Prerequisites

* [Create an Axiom account](https://app.axiom.co/register).
* [Create a dataset in Axiom](/reference/datasets#create-dataset) where you send your data.
* [Create an API token in Axiom](/reference/tokens) with permissions to update the dataset you have created.

## Query data with cURL

To query data with cURL:

1. Build the APL query. For more information, see [Introduction to APL](/apl/introduction).
2. Encode the APL query as a JSON object and enter it into the body of the API request.
3. Optional: In the body of the request, set optional parameters such as `startTime` and `endTime`. For more information, see the [query data API reference](/restapi/endpoints/queryApl).
4. Set the `Content-Type` header to `application/json`.
5. Set the `Authorization` header to `Bearer API_TOKEN`.
6. Send the POST request to one of the following:
   * For tabular output, use `https://AXIOM_DOMAIN/v1/datasets/_apl?format=tabular`.
   * For legacy output, use `https://AXIOM_DOMAIN/v1/datasets/_apl?format=legacy`.

### Example

```bash
curl --request POST \
  --url 'https://AXIOM_DOMAIN/v1/datasets/_apl?format=tabular' \
  --header 'Authorization: Bearer API_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
  "apl": "DATASET_NAME | limit 10",
  "startTime": "string",
  "endTime": "string"
}'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

**Example response**

```json [expandable]
{
  "format": "tabular",
  "status": {
    "elapsedTime": 260650,
    "minCursor": "0d8q6stroluyo-07c3957e7400015c-0000c875",
    "maxCursor": "0d8q6stroluyo-07c3957e7400015c-0000c877",
    "blocksExamined": 4,
    "blocksCached": 0,
    "blocksMatched": 0,
    "rowsExamined": 197604,
    "rowsMatched": 197604,
    "numGroups": 0,
    "isPartial": false,
    "cacheStatus": 1,
    "minBlockTime": "2025-03-26T12:03:14Z",
    "maxBlockTime": "2025-03-26T12:12:42Z"
  },
  "tables": [
    {
      "name": "0",
      "sources": [
        {
          "name": "DATASET_NAME"
        }
      ],
      "fields": [
        {
          "name": "_sysTime",
          "type": "datetime"
        },
        {
          "name": "_time",
          "type": "datetime"
        },
        {
          "name": "content_type",
          "type": "string"
        },
        {
          "name": "geo.city",
          "type": "string"
        },
        {
          "name": "geo.country",
          "type": "string"
        },
        {
          "name": "id",
          "type": "string"
        },
        {
          "name": "is_tls",
          "type": "boolean"
        },
        {
          "name": "message",
          "type": "string"
        },
        {
          "name": "method",
          "type": "string"
        },
        {
          "name": "req_duration_ms",
          "type": "float"
        },
        {
          "name": "resp_body_size_bytes",
          "type": "integer"
        },
        {
          "name": "resp_header_size_bytes",
          "type": "integer"
        },
        {
          "name": "server_datacenter",
          "type": "string"
        },
        {
          "name": "status",
          "type": "string"
        },
        {
          "name": "uri",
          "type": "string"
        },
        {
          "name": "user_agent",
          "type": "string"
        },
        {
          "name": "is_ok_2    ",
          "type": "boolean"
        },
        {
          "name": "city_str_len",
          "type": "integer"
        }
      ],
      "order": [
        {
          "field": "_time",
          "desc": true
        }
      ],
      "groups": [],
      "range": {
        "field": "_time",
        "start": "1970-01-01T00:00:00Z",
        "end": "2025-03-26T12:12:43Z"
      },
      "columns": [
        [
          "2025-03-26T12:12:42.68112905Z",
          "2025-03-26T12:12:42.68112905Z",
          "2025-03-26T12:12:42.68112905Z"
        ],
        [
          "2025-03-26T12:12:42Z",
          "2025-03-26T12:12:42Z",
          "2025-03-26T12:12:42Z"
        ],
        [
          "text/html",
          "text/plain-charset=utf-8",
          "image/jpeg"
        ],
        [
          "Ojinaga",
          "Humboldt",
          "Nevers"
        ],
        [
          "Mexico",
          "United States",
          "France"
        ],
        [
          "8af366cf-6f25-42e6-bbb4-d860ab535a60",
          "032e7f68-b0ab-47c0-a24a-35af566359e5",
          "4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9"
        ],
        [
          false,
          false,
          true
        ],
        [
          "QCD permutations were not solvable in linear time, expected compressed time",
          "QCD permutations were not solvable in linear time, expected compressed time",
          "Expected a new layer of particle physics but got a Higgs Boson"
        ],
        [
          "GET",
          "GET",
          "GET"
        ],
        [
          1.396373193863436,
          0.16252390534308514,
          0.4093416175186162
        ],
        [
          3448,
          2533,
          1906
        ],
        [
          84,
          31,
          29
        ],
        [
          "DCA",
          "GRU",
          "FRA"
        ],
        [
          "201",
          "200",
          "200"
        ],
        [
          "/api/v1/buy/commit/id/go",
          "/api/v1/textdata/cnfigs",
          "/api/v1/bank/warn"
        ],
        [
          "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
          "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
          "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))"
        ],
        [
          true,
          true,
          true
        ],
        [
          7,
          8,
          6
        ]
      ]
    }
  ],
  "datasetNames": [
    "DATASET_NAME"
  ],
  "fieldsMetaMap": {
    "DATASET_NAME": [
      {
        "name": "status",
        "type": "",
        "unit": "",
        "hidden": false,
        "description": "HTTP status code"
      },
      {
        "name": "resp_header_size_bytes",
        "type": "integer",
        "unit": "none",
        "hidden": false,
        "description": ""
      },
      {
        "name": "geo.city",
        "type": "string",
        "unit": "",
        "hidden": false,
        "description": "the city"
      },
      {
        "name": "resp_body_size_bytes",
        "type": "integer",
        "unit": "decbytes",
        "hidden": false,
        "description": ""
      },
      {
        "name": "content_type",
        "type": "string",
        "unit": "",
        "hidden": false,
        "description": ""
      },
      {
        "name": "geo.country",
        "type": "string",
        "unit": "",
        "hidden": false,
        "description": ""
      },
      {
        "name": "req_duration_ms",
        "type": "float",
        "unit": "ms",
        "hidden": false,
        "description": "Request duration"
      }
    ]
  }
}
```

## Query data with Axiom Node.js

1. [Install and configure](/guides/javascript#use-axiomhq-js) the Axiom Node.js library.
2. Build the APL query. For more information, see [Introduction to APL](/apl/introduction).
3. Pass the APL query as a string to the `axiom.query` function.

   ```ts
   const res = await axiom.query(`['DATASET_NAME'] | where foo == 'bar' | limit 100`);
   console.log(res);
   ```

   <Info>
     Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
   </Info>

For more examples, see the [examples in GitHub](https://github.com/axiomhq/axiom-js/tree/main/examples).

For more information on other libraries you can use to query data, see [Send data](send-data/methods).
# Pagination in Axiom API

> Learn how to use pagination with the Axiom API.

Pagination allows you to retrieve responses in manageable chunks.

You can use pagination for the following endpoints:

* [Run Query](/restapi/endpoints/queryApl)
* [Run Query (Legacy)](/restapi/endpoints/queryDataset)

## Prerequisites

* [Create an Axiom account](https://app.axiom.co/register).
* [Create a dataset in Axiom](/reference/datasets#create-dataset) where you send your data.
* [Create an API token in Axiom](/reference/tokens) with permissions to update the dataset you have created.

## Pagination mechanisms

You can use one of the following pagination mechanisms:

* [Pagination based on timestamp](#timestamp-based-pagination) (stable)
* [Pagination based on cursor](#cursor-based-pagination) (public preview)

Axiom recommends timestamp-based pagination. Cursor-based pagination is in public preview and may return unexpected query results.

## Timestamp-based pagination

The parameters and mechanisms differ between the current and legacy endpoints.

### Run Query

To use timestamp-based pagination with the Run Query endpoint:

* Include the [limit operator](/apl/tabular-operators/limit-operator) in the APL query of your API request. The argument of this operator determines the number of events to display per page.
* Use `sort by _time asc` or `sort by _time desc` in the APL query. This returns the results in ascending or descending chronological order. For more information, see [sort operator](/apl/tabular-operators/sort-operator).
* Specify `startTime` and `endTime` in the body of your API request.

### Run Query (Legacy)

To use timestamp-based pagination with the legacy Run Query endpoint:

* Add the `limit` parameter to the body of your API request. The value of this parameter determines the number of events to display per page.
* Add the `order` parameter to the body of your API request. In the value of this parameter, order the results by time in either ascending or descending chronological order. For example, `[{ "field": "_time", "desc": true }]`. For more information, see [order operator](/apl/tabular-operators/order-operator).
* Specify `startTime` and `endTime` in the body of your API request.

## Page through the result set

Use the timestamps as boundaries to page through the result set.

### Queries with descending order

To go to the next page of the result set for queries with descending order (`_time desc`):

1. Determine the timestamp of last item on the current page. This is the least recent event.
2. Optional: Subtract 1 nanosecond from the timestamp.
3. In your next request, change the value `endTime` parameter in the body of your API request to the timestamp of the last item (optionally, minus 1 nanosecond).

Repeat this process until the result set is empty.

### Queries with ascending order

To go to the next page of the result set for queries with ascending order (`_time asc`):

1. Determine the timestamp of last item on the current page. This is the most recent event.
2. Optional: Add 1 nanosecond to the timestamp.
3. In your next request, change the value `startTime` parameter in the body of your API request to the timestamp of the last item (optionally, plus 1 nanosecond).

Repeat this process until the result set is empty.

### Deduplication mechanism

In the procedures above, the steps about incrementing the timestamp are optional. If you increment the timestamp, there is a risk of duplication. If you don’t increment the timestamp, there is a risk of overlap. Duplicated data is possible for many reasons, such as backfill or natural duplication from external data sources. For these reasons, regardless of the method you choose (increment or not increment the timestamp, sort by descending or ascending order), Axiom recommends you implement some form of deduplication mechanism in your pagination script.

### Limits

Both the Run Query and the Run Query (Legacy) endpoints allow request-based limit configuration. This means that the limit they use is the lowest of the following: the query limit, the request limit, and Axiom’s server-side internal limit. Without a query or request limit, Axiom currently defaults to the limit of 1,000 events per page. For the pagination of datasets that are greater than 1,000 events, Axioms recommends specifying the same limit in the request and the APL query to avoid the default value and contradictory limits.

### Examples

#### Example request Run Query

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/_apl?format=tabular' \
-H 'Authorization: Bearer API_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
    "apl": "DATASET_NAME | sort by _time desc | limit 100",
    "startTime": "2024-11-30T00:00:00.000Z",
    "endTime": "2024-11-30T23:59:59.999Z"
  }'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

#### Example request Run Query (Legacy)

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/query' \
-H 'Authorization: Bearer API_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
    "startTime": "2024-11-30T00:00:00.000Z",
    "endTime": "2024-11-30T23:59:59.999Z",
    "limit": 100,
    "order": [{ "field": "_time", "desc": true }]
  }'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

#### Example request to page through the result set

Example request to go to next page for Run Query:

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/_apl?format=tabular' \
-H 'Authorization: Bearer API_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
    "apl": "DATASET_NAME | sort by _time desc | limit 100",
    "startTime": "2024-11-30T00:00:00.000Z",
    "endTime": "2024-11-30T22:59:59.999Z"
  }'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

Example request to go to next page for Run Query (Legacy):

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/query' \
-H 'Authorization: Bearer API_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
    "startTime": "2024-11-30T00:00:00.000Z",
    "endTime": "2024-11-30T22:59:59.999Z",
    "limit": 100,
    "order": [{ "field": "_time", "desc": true }]
  }'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

## Cursor-based pagination

Cursor-based pagination is in public preview and may return unexpected query results. Axiom recommends timestamp-based pagination.

The parameters and mechanisms differ between the current and legacy endpoints.

### Run Query

To use cursor-based pagination with the Run Query endpoint:

* Include the [`limit` operator](/apl/tabular-operators/limit-operator) in the APL query of your API request. The argument of this operator determines the number of events to display per page.
* Use `sort by _time asc` or `sort by _time desc` in the APL query. This returns the results in ascending or descending chronological order. For more information, see [sort operator](/apl/tabular-operators/sort-operator).
* Specify `startTime` and `endTime` in the body of your API request.

### Run Query (Legacy)

To use cursor-based pagination with the legacy Run Query endpoint:

* Add the `limit` parameter to the body of your API request. The value of this parameter determines the number of events to display per page.
* Add the `order` parameter to the body of your API request. In the value of this parameter, order the results by time in either ascending or descending chronological order. For example, `[{ "field": "_time", "desc": true }]`. For more information, see [order operator](/apl/tabular-operators/order-operator).
* Specify `startTime` and `endTime` in the body of your API request.

### Response format

<ResponseField name="status" type="object">
  Contains metadata about the response including pagination information.
</ResponseField>

<ResponseField name="status.minCursor" type="string">
  Cursor for the first item in the current page.
</ResponseField>

<ResponseField name="status.maxCursor" type="string">
  Cursor for the last item in the current page.
</ResponseField>

<ResponseField name="status.rowsMatched" type="integer">
  Total number of rows matching the query.
</ResponseField>

<ResponseField name="matches" type="array">
  Contains the list of returned objects.
</ResponseField>

## Page through the result set

To page through the result set, add the `cursor` parameter to the body of your API request.

<ParamField query="cursor" type="string">
  Optional. A cursor for use in pagination. Use the cursor string returned in previous responses to fetch the next or previous page of results.
</ParamField>

The `minCursor` and `maxCursor` fields in the response are boundaries that help you page through the result set.

For queries with descending order (`_time desc`), use `minCursor` from the response as the `cursor` in your next request to go to the next page. You reach the end when your provided `cursor` matches the `minCursor` in the response.

For queries with ascending order (`_time asc`), use `maxCursor` from the response as the `cursor` in your next request to go to the next page. You reach the end when your provided `cursor` matches the `maxCursor` in the response.

If the query returns fewer results than the specified limit, paging can stop.

### Examples

#### Example request Run Query

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/_apl?format=tabular' \
-H 'Authorization: Bearer API_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
    "apl": "DATASET_NAME | sort by _time desc | limit 100",
    "startTime": "2024-01-01T00:00:00.000Z",
    "endTime": "2024-01-31T23:59:59.999Z"
  }'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

#### Example request Run Query (Legacy)

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/query' \
-H 'Authorization: Bearer API_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
    "startTime": "2024-01-01T00:00:00.000Z",
    "endTime": "2024-01-31T23:59:59.999Z",
    "limit": 100,
    "order": [{ "field": "_time", "desc": true }]
  }'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

#### Example response

```json
{
  "status": {
    "rowsMatched": 2500,
    "minCursor": "0d3wo7v7e1oii-075a8c41710018b9-0000ecc5",
    "maxCursor": "0d3wo7v7e1oii-075a8c41710018b9-0000faa3"
  },
  "matches": [
    // ... events ...
  ]
}
```

#### Example request to page through the result set

To page through the result set, use the appropriate cursor value in your next request. For more information, see [Page through the result set](#page-through-the-result-set).

Example request to go to next page for Run Query:

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/_apl?format=tabular' \
-H 'Authorization: Bearer API_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
    "apl": "DATASET_NAME | sort by _time desc | limit 100",
    "startTime": "2024-01-01T00:00:00.000Z",
    "endTime": "2024-01-31T23:59:59.999Z",
    "cursor": "0d3wo7v7e1oii-075a8c41710018b9-0000ecc5"
  }'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>

Example request to go to next page for Run Query (Legacy):

```bash
curl -X 'POST' 'https://AXIOM_DOMAIN/v1/datasets/DATASET_NAME/query' \
-H 'Authorization: Bearer API_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
    "startTime": "2024-01-01T00:00:00.000Z",
    "endTime": "2024-01-31T23:59:59.999Z",
    "limit": 100,
    "order": [{ "field": "_time", "desc": true }],
    "cursor": "0d3wo7v7e1oii-075a8c41710018b9-0000ecc5"
  }'
```

<Info>
  Replace `AXIOM_DOMAIN` with `api.axiom.co` if your organization uses the US region, and with `api.eu.axiom.co` if your organization uses the EU region. For more information, see [Regions](/reference/regions).

  Replace `API_TOKEN` with the Axiom API token you have generated. For added security, store the API token in an environment variable.

  Replace `DATASET_NAME` with the name of the Axiom dataset where you send your data.
</Info>
# API limits

> Learn how to limit the number of calls a user can make over a certain period of time.

Axiom limits the number of calls a user (and their organization) can make over a certain period
of time to ensure fair usage and to maintain the quality of service for everyone.
Axiom systems closely monitor API usage and if a user exceeds any thresholds, Axiom
temporarily halts further processing of requests from that user (and/or organization).
This is to prevent any single user or app from overloading the system,
which could potentially impact other users' experience.

## Rate Limits

Rate limits vary and are specified by the following header in all responses:

| Header                  | Description                                                                                                             |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `X-RateLimit-Scope`     | Indicates if the limits counts against the organisation or personal rate limit.                                         |
| `X-RateLimit-Limit`     | The maximum number of requests a user is permitted to make per minute.                                                  |
| `X-RateLimit-Remaining` | The number of requests remaining in the current rate limit window.                                                      |
| `X-RateLimit-Reset`     | The time at which the current rate limit window resets in UTC [epoch seconds](https://en.wikipedia.org/wiki/Unix_time). |

**Possible values for X-RateLimit-Scope :**

* `user`
* `organization`

**When the rate limit is exceeded, an error is returned with the status "429 Too Many Requests"**:

```json
{
    "message": "rate limit exceeded",
}
```

## Query Limits

| Header                   | Description                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `X-QueryLimit-Limit`     | The query cost limit of your plan in Gigabyte Milliseconds (GB\*ms).                                                    |
| `X-QueryLimit-Remaining` | The remaining query Gigabyte Milliseconds.                                                                              |
| `X-QueryLimit-Reset`     | The time at which the current rate limit window resets in UTC [epoch seconds](https://en.wikipedia.org/wiki/Unix_time). |

## Ingest Limits

| Header                    | Description                                                                                                             |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `X-IngestLimit-Limit`     | The maximum bytes ingested a user is permitted to make per month.                                                       |
| `X-IngestLimit-Remaining` | The bytes ingested remaining in the current rate limit window.                                                          |
| `X-IngestLimit-Reset`     | The time at which the current rate limit window resets in UTC [epoch seconds](https://en.wikipedia.org/wiki/Unix_time). |

Alongside data volume limits, we also monitor the rate of ingest requests.
If an organization consistently sends an excessive number of requests per second,
far exceeding normal usage patterns, we reserve the right to suspend their ingest
to maintain system stability and ensure fair resource allocation for all users.
To prevent exceeding these rate limits, it’s highly recommended to use batching clients,
which can efficiently manage the number of requests by aggregating data before sending.

## Limits on ingested data

The table below summarizes the limits Axiom applies to each data ingest. These limits are independent of your pricing plan.

|                           | Limit     |
| ------------------------- | --------- |
| Maximum event size        | 1 MB      |
| Maximum events in a batch | 10,000    |
| Maximum field name length | 200 bytes |
 # API limits

> Learn how to limit the number of calls a user can make over a certain period of time.

Axiom limits the number of calls a user (and their organization) can make over a certain period
of time to ensure fair usage and to maintain the quality of service for everyone.
Axiom systems closely monitor API usage and if a user exceeds any thresholds, Axiom
temporarily halts further processing of requests from that user (and/or organization).
This is to prevent any single user or app from overloading the system,
which could potentially impact other users' experience.

## Rate Limits

Rate limits vary and are specified by the following header in all responses:

| Header                  | Description                                                                                                             |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `X-RateLimit-Scope`     | Indicates if the limits counts against the organisation or personal rate limit.                                         |
| `X-RateLimit-Limit`     | The maximum number of requests a user is permitted to make per minute.                                                  |
| `X-RateLimit-Remaining` | The number of requests remaining in the current rate limit window.                                                      |
| `X-RateLimit-Reset`     | The time at which the current rate limit window resets in UTC [epoch seconds](https://en.wikipedia.org/wiki/Unix_time). |

**Possible values for X-RateLimit-Scope :**

* `user`
* `organization`

**When the rate limit is exceeded, an error is returned with the status "429 Too Many Requests"**:

```json
{
    "message": "rate limit exceeded",
}
```

## Query Limits

| Header                   | Description                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `X-QueryLimit-Limit`     | The query cost limit of your plan in Gigabyte Milliseconds (GB\*ms).                                                    |
| `X-QueryLimit-Remaining` | The remaining query Gigabyte Milliseconds.                                                                              |
| `X-QueryLimit-Reset`     | The time at which the current rate limit window resets in UTC [epoch seconds](https://en.wikipedia.org/wiki/Unix_time). |

## Ingest Limits

| Header                    | Description                                                                                                             |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `X-IngestLimit-Limit`     | The maximum bytes ingested a user is permitted to make per month.                                                       |
| `X-IngestLimit-Remaining` | The bytes ingested remaining in the current rate limit window.                                                          |
| `X-IngestLimit-Reset`     | The time at which the current rate limit window resets in UTC [epoch seconds](https://en.wikipedia.org/wiki/Unix_time). |

Alongside data volume limits, we also monitor the rate of ingest requests.
If an organization consistently sends an excessive number of requests per second,
far exceeding normal usage patterns, we reserve the right to suspend their ingest
to maintain system stability and ensure fair resource allocation for all users.
To prevent exceeding these rate limits, it’s highly recommended to use batching clients,
which can efficiently manage the number of requests by aggregating data before sending.

## Limits on ingested data

The table below summarizes the limits Axiom applies to each data ingest. These limits are independent of your pricing plan.

|                           | Limit     |
| ------------------------- | --------- |
| Maximum event size        | 1 MB      |
| Maximum events in a batch | 10,000    |
| Maximum field name length | 200 bytes |
# Retrieve API token

> Get API token by ID

## OpenAPI

````yaml v2 get /tokens/{id}
paths:
  path: /tokens/{id}
  method: get
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path:
        id:
          schema:
            - type: string
              required: true
      query: {}
      header: {}
      cookie: {}
    body: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
        description: Token
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Create API token

> Create API token

## OpenAPI

````yaml v2 post /tokens
paths:
  path: /tokens
  method: post
  servers:
    - url: https://api.axiom.co/v2/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    nullable: true
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
            required: true
            refIdentifier: '#/components/schemas/CreateAPIToken'
            requiredProperties:
              - name
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              viewCapabilities: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              datasetCapabilities:
                allOf:
                  - $ref: '#/components/schemas/datasetCapabilities'
              description:
                allOf:
                  - description: Description of the token
                    type: string
              expiresAt:
                allOf:
                  - description: Expiration date of the token (ISO 8601 format)
                    type: string
                    format: date-time
                    readOnly: true
                    nullable: true
              id:
                allOf:
                  - description: ID of the token
                    type: string
              name:
                allOf:
                  - description: Name of the token
                    type: string
              orgCapabilities:
                allOf:
                  - $ref: '#/components/schemas/orgCapabilities'
              samlAuthenticated:
                allOf:
                  - type: boolean
              viewCapabilities:
                allOf:
                  - $ref: '#/components/schemas/viewCapabilities'
              token:
                allOf:
                  - type: string
                    x-go-name: Value
            refIdentifier: '#/components/schemas/APIToken'
            requiredProperties:
              - id
              - name
              - datasetCapabilities
              - orgCapabilities
        examples:
          example:
            value:
              datasetCapabilities: {}
              description: <string>
              expiresAt: '2023-11-07T05:31:56Z'
              id: <string>
              name: <string>
              orgCapabilities:
                annotations:
                  - create
                apiTokens:
                  - create
                auditLog:
                  - read
                billing:
                  - read
                dashboards:
                  - create
                datasets:
                  - create
                endpoints:
                  - create
                flows:
                  - create
                integrations:
                  - create
                monitors:
                  - create
                notifiers:
                  - create
                rbac:
                  - create
                sharedAccessKeys:
                  - read
                users:
                  - create
                views:
                  - create
              samlAuthenticated: true
              viewCapabilities: {}
              token: <string>
        description: CreateApiTokenResponse
  deprecated: false
  type: path
components:
  schemas:
    datasetCapabilities:
      type: object
      additionalProperties:
        properties:
          data:
            description: Data Management capability
            type: array
            items:
              type: string
              enum:
                - delete
            x-omitempty: true
          ingest:
            description: Ingest capability
            type: array
            items:
              type: string
              enum:
                - create
            x-omitempty: true
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing dataset capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true
          starredQueries:
            description: Starred queries capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
          trim:
            description: Data Trimming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          vacuum:
            description: Field Vacuuming capability
            type: array
            items:
              type: string
              enum:
                - update
            x-omitempty: true
          virtualFields:
            description: Virtual fields capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - update
                - delete
            x-omitempty: true
    orgCapabilities:
      type: object
      properties:
        annotations:
          description: Annotations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        apiTokens:
          description: API tokens capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        auditLog:
          description: Audit Log capability
          type: array
          items:
            type: string
            enum:
              - read
          x-omitempty: true
        billing:
          description: Billing capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        dashboards:
          description: Dashboards capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        datasets:
          description: Datasets capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        endpoints:
          description: Endpoints capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        flows:
          description: Flows capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        integrations:
          description: Integrations capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        monitors:
          description: Monitors capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        notifiers:
          description: Notifiers capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        rbac:
          description: Access control capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        sharedAccessKeys:
          description: Shared access keys capability
          type: array
          items:
            type: string
            enum:
              - read
              - update
          x-omitempty: true
        users:
          description: Users capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
        views:
          description: Views capability
          type: array
          items:
            type: string
            enum:
              - create
              - read
              - update
              - delete
          x-omitempty: true
    viewCapabilities:
      type: object
      additionalProperties:
        properties:
          query:
            description: Query capability
            type: array
            items:
              type: string
              enum:
                - read
            x-omitempty: true
          share:
            description: Sharing view capability
            type: array
            items:
              type: string
              enum:
                - create
                - read
                - delete
            x-omitempty: true

````# Run query

> Query

## OpenAPI

````yaml v1 post /datasets/_apl?format=tabular
paths:
  path: /datasets/_apl?format=tabular
  method: post
  servers:
    - url: https://api.axiom.co/v1/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query:
        format:
          schema:
            - type: enum<string>
              enum:
                - legacy
                - tabular
              required: true
        nocache:
          schema:
            - type: boolean
              default: false
        saveAsKind:
          schema:
            - type: string
        dataset_name:
          schema:
            - type: string
              description: >-
                When saveAsKind is true, this parameter indicates the name of
                the associated dataset.
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              apl:
                allOf:
                  - type: string
              cursor:
                allOf:
                  - type: string
              endTime:
                allOf:
                  - type: string
              includeCursor:
                allOf:
                  - type: boolean
              queryOptions:
                allOf:
                  - $ref: '#/components/schemas/QueryOptions'
              startTime:
                allOf:
                  - type: string
                    description: >-
                      start and end time for the query, these must be specified
                      as RFC3339 strings

                      or using relative time expressions (e.g. now-1h, now-1d,
                      now-1w, etc)
              variables:
                allOf:
                  - type: object
                    additionalProperties:
                      type: object
                      properties: {}
                    description: >-
                      Variables is an optional set of additional variables that
                      are inserted into the APL
            required: true
            refIdentifier: '#/components/schemas/APLRequestWithOptions'
            requiredProperties:
              - apl
            example:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
        examples:
          example:
            value:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              buckets:
                allOf:
                  - $ref: '#/components/schemas/Timeseries'
              datasetNames:
                allOf:
                  - type: array
                    items:
                      type: string
                    x-go-name: DatasetNames
              fieldsMetaMap:
                allOf:
                  - type: object
                    additionalProperties:
                      type: array
                      items:
                        $ref: '#/components/schemas/DatasetField'
                    description: >-
                      FieldsMetaMap contains the unit information (if we have
                      it) for each field in the given dataset entry
                    x-go-name: FieldsMetaMap
              format:
                allOf:
                  - type: string
                    description: >-
                      Format specifies the result set format. Either "legacy"
                      (default) or "tabular".
                    x-go-name: Format
              matches:
                allOf:
                  - type: array
                    description: >-
                      Matches hold the matching events of a filter query in the
                      "legacy" result format
                    items:
                      $ref: '#/components/schemas/Entry'
                    x-go-name: Matches
              request:
                allOf:
                  - $ref: '#/components/schemas/QueryRequest'
              status:
                allOf:
                  - $ref: '#/components/schemas/Status'
              tables:
                allOf:
                  - type: array
                    description: >-
                      Tables hold the result tables in the "tabular" result
                      format
                    items:
                      $ref: '#/components/schemas/Table'
                    x-go-name: Tables
            refIdentifier: '#/components/schemas/AplResult'
            requiredProperties:
              - datasetNames
              - format
              - status
            example:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        examples:
          example:
            value:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        description: Successful APL result
    '403':
      application/json:
        schemaArray:
          - type: object
            properties:
              code:
                allOf:
                  - type: string
              message:
                allOf:
                  - type: string
            refIdentifier: '#/components/schemas/ForbiddenError'
            example:
              code: 403
              message: Forbidden
        examples:
          example:
            value:
              code: 403
              message: Forbidden
        description: Forbidden
  deprecated: false
  type: path
components:
  schemas:
    AggInfo:
      required:
        - name
      type: object
      properties:
        args:
          type: array
          description: >-
            Args specifies any non-field arguments for the aggregation. Fx. [10]
            for topk(players, 10).
          items:
            type: object
            properties: {}
          x-go-name: Args
        fields:
          type: array
          description: >-
            Fields specifies the names of the fields this aggregation is
            computed on.

            Fx ["players"] for topk(players, 10)
          items:
            type: string
          x-go-name: Fields
        name:
          type: string
          description: >-
            Name is the system name of the aggregation, which is the string form
            of aggregation.Type.

            If the aggregation is aliased, the alias is stored in the parent
            FieldInfo
          x-go-name: Name
      description: AggInfo captures information about an aggregation
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: AggInfo
    Aggregation:
      required:
        - field
        - op
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        argument:
          type: object
          properties: {}
          x-go-name: Argument
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          enum:
            - count
            - distinct
            - sum
            - avg
            - min
            - max
            - topk
            - percentiles
            - histogram
            - stdev
            - variance
            - argmin
            - argmax
            - makeset
            - rate
            - makelist
          x-go-name: Op
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Aggregation
    BucketInfo:
      required:
        - field
        - size
      title: >-
        BucketInfo captures information about how a grouped query is sorted into
        buckets.
      type: object
      properties:
        field:
          type: string
          description: >-
            Field specifies the field used to create buckets on. Normally this
            would be _time.
          x-go-name: Field
        size:
          type: object
          properties: {}
          description: |-
            An integer or float representing the fixed bucket size.
            When the bucket field is _time this value is in nanoseconds.
          x-go-name: Size
      description: The standard mode of operation is to create buckets on the _time column,
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: BucketInfo
    DatasetField:
      required:
        - hidden
        - name
        - type
        - unit
      type: object
      properties:
        description:
          type: string
          x-go-name: Description
        hidden:
          type: boolean
          x-go-name: Hidden
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
        unit:
          type: string
          x-go-name: Unit
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: DatasetField
    Entry:
      required:
        - _rowId
        - _sysTime
        - _time
        - data
      type: object
      properties:
        _rowId:
          type: string
          x-go-name: RowID
        _sysTime:
          type: string
          format: date-time
          x-go-name: SysTime
        _time:
          type: string
          format: date-time
          x-go-name: Time
        data:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Data
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Entry
    EntryGroup:
      required:
        - group
        - id
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroupAgg'
          x-go-name: Aggregations
        group:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Group
        id:
          type: integer
          format: uint64
          x-go-name: ID
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroup
    EntryGroupAgg:
      required:
        - op
        - value
      type: object
      properties:
        data:
          type: object
          properties: {}
          x-go-name: Data
        op:
          type: string
          x-go-name: Alias
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroupAgg
    FieldInfo:
      required:
        - name
        - type
      title: >-
        FieldInfo captures information about a field used in the tabular result
        format. See Table.
      type: object
      properties:
        agg:
          $ref: '#/components/schemas/AggInfo'
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: FieldInfo
    Filter:
      required:
        - field
        - op
      type: object
      properties:
        caseSensitive:
          type: boolean
          description: >-
            Supported for these filters: starts-with, not-starts-with,
            ends-with, not-ends-with, contains, not-contains, eq, ne.
          x-go-name: CaseSensitive
        children:
          type: array
          description: 'Supported for these filters: and, or, not.'
          items:
            type: string
          x-go-name: Children
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          description: >-
            We also support '==', but we’re not exporting that to swagger,
            because it can’t deal with it add >, >=, <, <= to that list, it
            breaks codegen.
          enum:
            - and
            - or
            - not
            - eq
            - '!='
            - ne
            - exists
            - not-exists
            - gt
            - gte
            - lt
            - lte
            - starts-with
            - not-starts-with
            - ends-with
            - not-ends-with
            - contains
            - not-contains
            - regexp
            - not-regexp
          x-go-name: Op
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Filter
    GroupInfo:
      title: >-
        GroupInfo captures information about a grouping clause in the tabular
        result format. See Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: GroupInfo
    Interval:
      required:
        - endTime
        - startTime
      type: object
      properties:
        endTime:
          type: string
          format: date-time
          x-go-name: EndTime
        groups:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Groups
        startTime:
          type: string
          format: date-time
          x-go-name: StartTime
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Interval
    Message:
      required:
        - count
        - msg
        - priority
      type: object
      properties:
        code:
          type: string
          x-go-name: Code
        count:
          type: integer
          format: int64
          x-go-name: Count
        msg:
          type: string
          x-go-name: Msg
        priority:
          type: string
          x-go-name: Priority
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Message
    Order:
      required:
        - desc
        - field
      type: object
      properties:
        desc:
          type: boolean
          x-go-name: Desc
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Order
    Projection:
      required:
        - field
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Projection
    QueryOptions:
      type: object
      properties:
        against:
          type: string
        againstStart:
          type: string
        againstTimestamp:
          type: string
        aggChartOpts:
          type: string
        caseSensitive:
          type: string
        containsTimeFilter:
          type: string
        datasets:
          type: string
        displayNull:
          type: string
        editorContent:
          type: string
        endColumn:
          type: string
        endLineNumber:
          type: string
        endTime:
          type: string
        integrationsFilter:
          type: string
        openIntervals:
          type: string
        quickRange:
          type: string
        resolution:
          type: string
        shownColumns:
          type: string
        startColumn:
          type: string
        startLineNumber:
          type: string
        startTime:
          type: string
        timeSeriesVariant:
          type: string
        timeSeriesView:
          type: string
    QueryRequest:
      required:
        - endTime
        - resolution
        - startTime
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/Aggregation'
          x-go-name: Aggregations
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        cursor:
          type: string
          x-go-name: Cursor
        endTime:
          type: string
          x-go-name: EndTime
        fieldsMeta:
          type: array
          description: >-
            FieldsMeta contains the unit information (if we have it) for each
            field
          items:
            $ref: '#/components/schemas/DatasetField'
          x-go-name: FieldsMeta
        filter:
          $ref: '#/components/schemas/Filter'
        groupBy:
          type: array
          items:
            type: string
          x-go-name: GroupBy
        includeCursor:
          type: boolean
          x-go-name: IncludeCursor
        limit:
          type: integer
          format: uint32
          x-go-name: Limit
        order:
          type: array
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        project:
          type: array
          items:
            $ref: '#/components/schemas/Projection'
          x-go-name: Project
        resolution:
          type: string
          description: >-
            The time resolution of the query’s graph, in seconds. Valid values
            are

            the query’s time range /100 at maximum and /1000 at minimum or
            "auto".
          x-go-name: Resolution
        startTime:
          type: string
          description: >-
            start and end time for the query, these must be specified as RFC3339
            strings

            or using relative time expressions (e.g. now-1h, now-1d, now-1w,
            etc)
          x-go-name: StartTime
        virtualFields:
          type: array
          items:
            $ref: '#/components/schemas/VirtualColumn'
          x-go-name: VirtualColumns
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: QueryRequest
    RangeInfo:
      required:
        - field
        - start
        - end
      title: RangeInfo specifies the window a query was restricted to.
      type: object
      properties:
        end:
          type: string
          description: |-
            End is the ending time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: End
        field:
          type: string
          description: >-
            Field specifies the field name on which the query range was
            restricted. Normally _time
          x-go-name: Field
        start:
          type: string
          description: |-
            Start is the starting time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: Start
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: RangeInfo
    SourceInfo:
      required:
        - name
      title: SourceInfo specifies the provenance of a results Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      description: >-
        Result sources will typically be the names of a datasets that were
        searched,

        but may be expanded to other things in the future.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: SourceInfo
    Status:
      required:
        - blocksExamined
        - cacheStatus
        - elapsedTime
        - isPartial
        - maxBlockTime
        - minBlockTime
        - numGroups
        - rowsExamined
        - rowsMatched
      type: object
      properties:
        blocksExamined:
          type: integer
          format: uint64
          x-go-name: BlocksExamined
        cacheStatus:
          type: integer
          format: uint8
          x-go-name: CacheStatus
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        elapsedTime:
          type: integer
          format: int64
          x-go-name: ElapsedTime
        isEstimate:
          type: boolean
          x-go-name: IsEstimate
        isPartial:
          type: boolean
          x-go-name: IsPartial
        maxBlockTime:
          type: string
          format: date-time
          x-go-name: MaxBlockTime
        maxCursor:
          type: string
          description: >-
            Row id of the newest row, as seen server side.

            May be higher than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MaxCursor
        messages:
          type: array
          items:
            $ref: '#/components/schemas/Message'
          x-go-name: Messages
        minBlockTime:
          type: string
          format: date-time
          x-go-name: MinBlockTime
        minCursor:
          type: string
          description: >-
            Row id of the oldest row, as seen server side.

            May be lower than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MinCursor
        numGroups:
          type: integer
          format: uint32
          x-go-name: NumGroups
        rowsExamined:
          type: integer
          format: uint64
          x-go-name: RowsExamined
        rowsMatched:
          type: integer
          format: uint64
          x-go-name: RowsMatched
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Status
    Table:
      required:
        - name
        - sources
        - fields
        - order
        - groups
      title: >-
        Table defines the schema for query results in the "tabular" result
        format.
      type: object
      properties:
        buckets:
          $ref: '#/components/schemas/BucketInfo'
        columns:
          type: array
          description: |-
            Columns contain a series of arrays with the raw result data.
            The columns here line up with the fields in the Fields array.
          items:
            type: array
            items:
              type: object
              properties: {}
          x-go-name: Columns
        fields:
          type: array
          description: >-
            Fields contain information about the fields included in these
            results.

            The order of the fields match up with the order of the data in
            Columns.
          items:
            $ref: '#/components/schemas/FieldInfo'
          x-go-name: Fields
        groups:
          type: array
          description: >-
            Groups specifies which grouping operations has been performed on the
            results.
          items:
            $ref: '#/components/schemas/GroupInfo'
          x-go-name: GroupBy
        name:
          type: string
          description: >-
            Name is the name assigned to this table. Defaults to "0". The name
            "_totals" is reserved for system use.
          x-go-name: Name
        order:
          type: array
          description: Order echoes the ordering clauses that was used to sort the results.
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        range:
          $ref: '#/components/schemas/RangeInfo'
        sources:
          type: array
          description: >-
            Sources contain the names of the datasets that contributed data to
            these results.
          items:
            $ref: '#/components/schemas/SourceInfo'
          x-go-name: Sources
      description: >-
        The tabular result format can be enabled via APLQueryParams.ResultFormat
        or QueryParams.ResultFormat.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Table
    Timeseries:
      type: object
      properties:
        series:
          type: array
          items:
            $ref: '#/components/schemas/Interval'
          x-go-name: Series
        totals:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Totals
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Timeseries
    VirtualColumn:
      required:
        - alias
        - expr
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        expr:
          type: string
          x-go-name: Expr
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: VirtualColumn

````# Run query

> Query

## OpenAPI

````yaml v1 post /datasets/_apl?format=tabular
paths:
  path: /datasets/_apl?format=tabular
  method: post
  servers:
    - url: https://api.axiom.co/v1/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query:
        format:
          schema:
            - type: enum<string>
              enum:
                - legacy
                - tabular
              required: true
        nocache:
          schema:
            - type: boolean
              default: false
        saveAsKind:
          schema:
            - type: string
        dataset_name:
          schema:
            - type: string
              description: >-
                When saveAsKind is true, this parameter indicates the name of
                the associated dataset.
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              apl:
                allOf:
                  - type: string
              cursor:
                allOf:
                  - type: string
              endTime:
                allOf:
                  - type: string
              includeCursor:
                allOf:
                  - type: boolean
              queryOptions:
                allOf:
                  - $ref: '#/components/schemas/QueryOptions'
              startTime:
                allOf:
                  - type: string
                    description: >-
                      start and end time for the query, these must be specified
                      as RFC3339 strings

                      or using relative time expressions (e.g. now-1h, now-1d,
                      now-1w, etc)
              variables:
                allOf:
                  - type: object
                    additionalProperties:
                      type: object
                      properties: {}
                    description: >-
                      Variables is an optional set of additional variables that
                      are inserted into the APL
            required: true
            refIdentifier: '#/components/schemas/APLRequestWithOptions'
            requiredProperties:
              - apl
            example:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
        examples:
          example:
            value:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              buckets:
                allOf:
                  - $ref: '#/components/schemas/Timeseries'
              datasetNames:
                allOf:
                  - type: array
                    items:
                      type: string
                    x-go-name: DatasetNames
              fieldsMetaMap:
                allOf:
                  - type: object
                    additionalProperties:
                      type: array
                      items:
                        $ref: '#/components/schemas/DatasetField'
                    description: >-
                      FieldsMetaMap contains the unit information (if we have
                      it) for each field in the given dataset entry
                    x-go-name: FieldsMetaMap
              format:
                allOf:
                  - type: string
                    description: >-
                      Format specifies the result set format. Either "legacy"
                      (default) or "tabular".
                    x-go-name: Format
              matches:
                allOf:
                  - type: array
                    description: >-
                      Matches hold the matching events of a filter query in the
                      "legacy" result format
                    items:
                      $ref: '#/components/schemas/Entry'
                    x-go-name: Matches
              request:
                allOf:
                  - $ref: '#/components/schemas/QueryRequest'
              status:
                allOf:
                  - $ref: '#/components/schemas/Status'
              tables:
                allOf:
                  - type: array
                    description: >-
                      Tables hold the result tables in the "tabular" result
                      format
                    items:
                      $ref: '#/components/schemas/Table'
                    x-go-name: Tables
            refIdentifier: '#/components/schemas/AplResult'
            requiredProperties:
              - datasetNames
              - format
              - status
            example:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        examples:
          example:
            value:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        description: Successful APL result
    '403':
      application/json:
        schemaArray:
          - type: object
            properties:
              code:
                allOf:
                  - type: string
              message:
                allOf:
                  - type: string
            refIdentifier: '#/components/schemas/ForbiddenError'
            example:
              code: 403
              message: Forbidden
        examples:
          example:
            value:
              code: 403
              message: Forbidden
        description: Forbidden
  deprecated: false
  type: path
components:
  schemas:
    AggInfo:
      required:
        - name
      type: object
      properties:
        args:
          type: array
          description: >-
            Args specifies any non-field arguments for the aggregation. Fx. [10]
            for topk(players, 10).
          items:
            type: object
            properties: {}
          x-go-name: Args
        fields:
          type: array
          description: >-
            Fields specifies the names of the fields this aggregation is
            computed on.

            Fx ["players"] for topk(players, 10)
          items:
            type: string
          x-go-name: Fields
        name:
          type: string
          description: >-
            Name is the system name of the aggregation, which is the string form
            of aggregation.Type.

            If the aggregation is aliased, the alias is stored in the parent
            FieldInfo
          x-go-name: Name
      description: AggInfo captures information about an aggregation
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: AggInfo
    Aggregation:
      required:
        - field
        - op
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        argument:
          type: object
          properties: {}
          x-go-name: Argument
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          enum:
            - count
            - distinct
            - sum
            - avg
            - min
            - max
            - topk
            - percentiles
            - histogram
            - stdev
            - variance
            - argmin
            - argmax
            - makeset
            - rate
            - makelist
          x-go-name: Op
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Aggregation
    BucketInfo:
      required:
        - field
        - size
      title: >-
        BucketInfo captures information about how a grouped query is sorted into
        buckets.
      type: object
      properties:
        field:
          type: string
          description: >-
            Field specifies the field used to create buckets on. Normally this
            would be _time.
          x-go-name: Field
        size:
          type: object
          properties: {}
          description: |-
            An integer or float representing the fixed bucket size.
            When the bucket field is _time this value is in nanoseconds.
          x-go-name: Size
      description: The standard mode of operation is to create buckets on the _time column,
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: BucketInfo
    DatasetField:
      required:
        - hidden
        - name
        - type
        - unit
      type: object
      properties:
        description:
          type: string
          x-go-name: Description
        hidden:
          type: boolean
          x-go-name: Hidden
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
        unit:
          type: string
          x-go-name: Unit
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: DatasetField
    Entry:
      required:
        - _rowId
        - _sysTime
        - _time
        - data
      type: object
      properties:
        _rowId:
          type: string
          x-go-name: RowID
        _sysTime:
          type: string
          format: date-time
          x-go-name: SysTime
        _time:
          type: string
          format: date-time
          x-go-name: Time
        data:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Data
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Entry
    EntryGroup:
      required:
        - group
        - id
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroupAgg'
          x-go-name: Aggregations
        group:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Group
        id:
          type: integer
          format: uint64
          x-go-name: ID
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroup
    EntryGroupAgg:
      required:
        - op
        - value
      type: object
      properties:
        data:
          type: object
          properties: {}
          x-go-name: Data
        op:
          type: string
          x-go-name: Alias
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroupAgg
    FieldInfo:
      required:
        - name
        - type
      title: >-
        FieldInfo captures information about a field used in the tabular result
        format. See Table.
      type: object
      properties:
        agg:
          $ref: '#/components/schemas/AggInfo'
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: FieldInfo
    Filter:
      required:
        - field
        - op
      type: object
      properties:
        caseSensitive:
          type: boolean
          description: >-
            Supported for these filters: starts-with, not-starts-with,
            ends-with, not-ends-with, contains, not-contains, eq, ne.
          x-go-name: CaseSensitive
        children:
          type: array
          description: 'Supported for these filters: and, or, not.'
          items:
            type: string
          x-go-name: Children
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          description: >-
            We also support '==', but we’re not exporting that to swagger,
            because it can’t deal with it add >, >=, <, <= to that list, it
            breaks codegen.
          enum:
            - and
            - or
            - not
            - eq
            - '!='
            - ne
            - exists
            - not-exists
            - gt
            - gte
            - lt
            - lte
            - starts-with
            - not-starts-with
            - ends-with
            - not-ends-with
            - contains
            - not-contains
            - regexp
            - not-regexp
          x-go-name: Op
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Filter
    GroupInfo:
      title: >-
        GroupInfo captures information about a grouping clause in the tabular
        result format. See Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: GroupInfo
    Interval:
      required:
        - endTime
        - startTime
      type: object
      properties:
        endTime:
          type: string
          format: date-time
          x-go-name: EndTime
        groups:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Groups
        startTime:
          type: string
          format: date-time
          x-go-name: StartTime
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Interval
    Message:
      required:
        - count
        - msg
        - priority
      type: object
      properties:
        code:
          type: string
          x-go-name: Code
        count:
          type: integer
          format: int64
          x-go-name: Count
        msg:
          type: string
          x-go-name: Msg
        priority:
          type: string
          x-go-name: Priority
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Message
    Order:
      required:
        - desc
        - field
      type: object
      properties:
        desc:
          type: boolean
          x-go-name: Desc
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Order
    Projection:
      required:
        - field
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Projection
    QueryOptions:
      type: object
      properties:
        against:
          type: string
        againstStart:
          type: string
        againstTimestamp:
          type: string
        aggChartOpts:
          type: string
        caseSensitive:
          type: string
        containsTimeFilter:
          type: string
        datasets:
          type: string
        displayNull:
          type: string
        editorContent:
          type: string
        endColumn:
          type: string
        endLineNumber:
          type: string
        endTime:
          type: string
        integrationsFilter:
          type: string
        openIntervals:
          type: string
        quickRange:
          type: string
        resolution:
          type: string
        shownColumns:
          type: string
        startColumn:
          type: string
        startLineNumber:
          type: string
        startTime:
          type: string
        timeSeriesVariant:
          type: string
        timeSeriesView:
          type: string
    QueryRequest:
      required:
        - endTime
        - resolution
        - startTime
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/Aggregation'
          x-go-name: Aggregations
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        cursor:
          type: string
          x-go-name: Cursor
        endTime:
          type: string
          x-go-name: EndTime
        fieldsMeta:
          type: array
          description: >-
            FieldsMeta contains the unit information (if we have it) for each
            field
          items:
            $ref: '#/components/schemas/DatasetField'
          x-go-name: FieldsMeta
        filter:
          $ref: '#/components/schemas/Filter'
        groupBy:
          type: array
          items:
            type: string
          x-go-name: GroupBy
        includeCursor:
          type: boolean
          x-go-name: IncludeCursor
        limit:
          type: integer
          format: uint32
          x-go-name: Limit
        order:
          type: array
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        project:
          type: array
          items:
            $ref: '#/components/schemas/Projection'
          x-go-name: Project
        resolution:
          type: string
          description: >-
            The time resolution of the query’s graph, in seconds. Valid values
            are

            the query’s time range /100 at maximum and /1000 at minimum or
            "auto".
          x-go-name: Resolution
        startTime:
          type: string
          description: >-
            start and end time for the query, these must be specified as RFC3339
            strings

            or using relative time expressions (e.g. now-1h, now-1d, now-1w,
            etc)
          x-go-name: StartTime
        virtualFields:
          type: array
          items:
            $ref: '#/components/schemas/VirtualColumn'
          x-go-name: VirtualColumns
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: QueryRequest
    RangeInfo:
      required:
        - field
        - start
        - end
      title: RangeInfo specifies the window a query was restricted to.
      type: object
      properties:
        end:
          type: string
          description: |-
            End is the ending time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: End
        field:
          type: string
          description: >-
            Field specifies the field name on which the query range was
            restricted. Normally _time
          x-go-name: Field
        start:
          type: string
          description: |-
            Start is the starting time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: Start
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: RangeInfo
    SourceInfo:
      required:
        - name
      title: SourceInfo specifies the provenance of a results Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      description: >-
        Result sources will typically be the names of a datasets that were
        searched,

        but may be expanded to other things in the future.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: SourceInfo
    Status:
      required:
        - blocksExamined
        - cacheStatus
        - elapsedTime
        - isPartial
        - maxBlockTime
        - minBlockTime
        - numGroups
        - rowsExamined
        - rowsMatched
      type: object
      properties:
        blocksExamined:
          type: integer
          format: uint64
          x-go-name: BlocksExamined
        cacheStatus:
          type: integer
          format: uint8
          x-go-name: CacheStatus
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        elapsedTime:
          type: integer
          format: int64
          x-go-name: ElapsedTime
        isEstimate:
          type: boolean
          x-go-name: IsEstimate
        isPartial:
          type: boolean
          x-go-name: IsPartial
        maxBlockTime:
          type: string
          format: date-time
          x-go-name: MaxBlockTime
        maxCursor:
          type: string
          description: >-
            Row id of the newest row, as seen server side.

            May be higher than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MaxCursor
        messages:
          type: array
          items:
            $ref: '#/components/schemas/Message'
          x-go-name: Messages
        minBlockTime:
          type: string
          format: date-time
          x-go-name: MinBlockTime
        minCursor:
          type: string
          description: >-
            Row id of the oldest row, as seen server side.

            May be lower than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MinCursor
        numGroups:
          type: integer
          format: uint32
          x-go-name: NumGroups
        rowsExamined:
          type: integer
          format: uint64
          x-go-name: RowsExamined
        rowsMatched:
          type: integer
          format: uint64
          x-go-name: RowsMatched
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Status
    Table:
      required:
        - name
        - sources
        - fields
        - order
        - groups
      title: >-
        Table defines the schema for query results in the "tabular" result
        format.
      type: object
      properties:
        buckets:
          $ref: '#/components/schemas/BucketInfo'
        columns:
          type: array
          description: |-
            Columns contain a series of arrays with the raw result data.
            The columns here line up with the fields in the Fields array.
          items:
            type: array
            items:
              type: object
              properties: {}
          x-go-name: Columns
        fields:
          type: array
          description: >-
            Fields contain information about the fields included in these
            results.

            The order of the fields match up with the order of the data in
            Columns.
          items:
            $ref: '#/components/schemas/FieldInfo'
          x-go-name: Fields
        groups:
          type: array
          description: >-
            Groups specifies which grouping operations has been performed on the
            results.
          items:
            $ref: '#/components/schemas/GroupInfo'
          x-go-name: GroupBy
        name:
          type: string
          description: >-
            Name is the name assigned to this table. Defaults to "0". The name
            "_totals" is reserved for system use.
          x-go-name: Name
        order:
          type: array
          description: Order echoes the ordering clauses that was used to sort the results.
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        range:
          $ref: '#/components/schemas/RangeInfo'
        sources:
          type: array
          description: >-
            Sources contain the names of the datasets that contributed data to
            these results.
          items:
            $ref: '#/components/schemas/SourceInfo'
          x-go-name: Sources
      description: >-
        The tabular result format can be enabled via APLQueryParams.ResultFormat
        or QueryParams.ResultFormat.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Table
    Timeseries:
      type: object
      properties:
        series:
          type: array
          items:
            $ref: '#/components/schemas/Interval'
          x-go-name: Series
        totals:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Totals
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Timeseries
    VirtualColumn:
      required:
        - alias
        - expr
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        expr:
          type: string
          x-go-name: Expr
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: VirtualColumn

````# Run query

> Query

## OpenAPI

````yaml v1 post /datasets/_apl?format=tabular
paths:
  path: /datasets/_apl?format=tabular
  method: post
  servers:
    - url: https://api.axiom.co/v1/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query:
        format:
          schema:
            - type: enum<string>
              enum:
                - legacy
                - tabular
              required: true
        nocache:
          schema:
            - type: boolean
              default: false
        saveAsKind:
          schema:
            - type: string
        dataset_name:
          schema:
            - type: string
              description: >-
                When saveAsKind is true, this parameter indicates the name of
                the associated dataset.
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              apl:
                allOf:
                  - type: string
              cursor:
                allOf:
                  - type: string
              endTime:
                allOf:
                  - type: string
              includeCursor:
                allOf:
                  - type: boolean
              queryOptions:
                allOf:
                  - $ref: '#/components/schemas/QueryOptions'
              startTime:
                allOf:
                  - type: string
                    description: >-
                      start and end time for the query, these must be specified
                      as RFC3339 strings

                      or using relative time expressions (e.g. now-1h, now-1d,
                      now-1w, etc)
              variables:
                allOf:
                  - type: object
                    additionalProperties:
                      type: object
                      properties: {}
                    description: >-
                      Variables is an optional set of additional variables that
                      are inserted into the APL
            required: true
            refIdentifier: '#/components/schemas/APLRequestWithOptions'
            requiredProperties:
              - apl
            example:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
        examples:
          example:
            value:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              buckets:
                allOf:
                  - $ref: '#/components/schemas/Timeseries'
              datasetNames:
                allOf:
                  - type: array
                    items:
                      type: string
                    x-go-name: DatasetNames
              fieldsMetaMap:
                allOf:
                  - type: object
                    additionalProperties:
                      type: array
                      items:
                        $ref: '#/components/schemas/DatasetField'
                    description: >-
                      FieldsMetaMap contains the unit information (if we have
                      it) for each field in the given dataset entry
                    x-go-name: FieldsMetaMap
              format:
                allOf:
                  - type: string
                    description: >-
                      Format specifies the result set format. Either "legacy"
                      (default) or "tabular".
                    x-go-name: Format
              matches:
                allOf:
                  - type: array
                    description: >-
                      Matches hold the matching events of a filter query in the
                      "legacy" result format
                    items:
                      $ref: '#/components/schemas/Entry'
                    x-go-name: Matches
              request:
                allOf:
                  - $ref: '#/components/schemas/QueryRequest'
              status:
                allOf:
                  - $ref: '#/components/schemas/Status'
              tables:
                allOf:
                  - type: array
                    description: >-
                      Tables hold the result tables in the "tabular" result
                      format
                    items:
                      $ref: '#/components/schemas/Table'
                    x-go-name: Tables
            refIdentifier: '#/components/schemas/AplResult'
            requiredProperties:
              - datasetNames
              - format
              - status
            example:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        examples:
          example:
            value:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        description: Successful APL result
    '403':
      application/json:
        schemaArray:
          - type: object
            properties:
              code:
                allOf:
                  - type: string
              message:
                allOf:
                  - type: string
            refIdentifier: '#/components/schemas/ForbiddenError'
            example:
              code: 403
              message: Forbidden
        examples:
          example:
            value:
              code: 403
              message: Forbidden
        description: Forbidden
  deprecated: false
  type: path
components:
  schemas:
    AggInfo:
      required:
        - name
      type: object
      properties:
        args:
          type: array
          description: >-
            Args specifies any non-field arguments for the aggregation. Fx. [10]
            for topk(players, 10).
          items:
            type: object
            properties: {}
          x-go-name: Args
        fields:
          type: array
          description: >-
            Fields specifies the names of the fields this aggregation is
            computed on.

            Fx ["players"] for topk(players, 10)
          items:
            type: string
          x-go-name: Fields
        name:
          type: string
          description: >-
            Name is the system name of the aggregation, which is the string form
            of aggregation.Type.

            If the aggregation is aliased, the alias is stored in the parent
            FieldInfo
          x-go-name: Name
      description: AggInfo captures information about an aggregation
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: AggInfo
    Aggregation:
      required:
        - field
        - op
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        argument:
          type: object
          properties: {}
          x-go-name: Argument
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          enum:
            - count
            - distinct
            - sum
            - avg
            - min
            - max
            - topk
            - percentiles
            - histogram
            - stdev
            - variance
            - argmin
            - argmax
            - makeset
            - rate
            - makelist
          x-go-name: Op
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Aggregation
    BucketInfo:
      required:
        - field
        - size
      title: >-
        BucketInfo captures information about how a grouped query is sorted into
        buckets.
      type: object
      properties:
        field:
          type: string
          description: >-
            Field specifies the field used to create buckets on. Normally this
            would be _time.
          x-go-name: Field
        size:
          type: object
          properties: {}
          description: |-
            An integer or float representing the fixed bucket size.
            When the bucket field is _time this value is in nanoseconds.
          x-go-name: Size
      description: The standard mode of operation is to create buckets on the _time column,
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: BucketInfo
    DatasetField:
      required:
        - hidden
        - name
        - type
        - unit
      type: object
      properties:
        description:
          type: string
          x-go-name: Description
        hidden:
          type: boolean
          x-go-name: Hidden
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
        unit:
          type: string
          x-go-name: Unit
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: DatasetField
    Entry:
      required:
        - _rowId
        - _sysTime
        - _time
        - data
      type: object
      properties:
        _rowId:
          type: string
          x-go-name: RowID
        _sysTime:
          type: string
          format: date-time
          x-go-name: SysTime
        _time:
          type: string
          format: date-time
          x-go-name: Time
        data:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Data
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Entry
    EntryGroup:
      required:
        - group
        - id
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroupAgg'
          x-go-name: Aggregations
        group:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Group
        id:
          type: integer
          format: uint64
          x-go-name: ID
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroup
    EntryGroupAgg:
      required:
        - op
        - value
      type: object
      properties:
        data:
          type: object
          properties: {}
          x-go-name: Data
        op:
          type: string
          x-go-name: Alias
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroupAgg
    FieldInfo:
      required:
        - name
        - type
      title: >-
        FieldInfo captures information about a field used in the tabular result
        format. See Table.
      type: object
      properties:
        agg:
          $ref: '#/components/schemas/AggInfo'
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: FieldInfo
    Filter:
      required:
        - field
        - op
      type: object
      properties:
        caseSensitive:
          type: boolean
          description: >-
            Supported for these filters: starts-with, not-starts-with,
            ends-with, not-ends-with, contains, not-contains, eq, ne.
          x-go-name: CaseSensitive
        children:
          type: array
          description: 'Supported for these filters: and, or, not.'
          items:
            type: string
          x-go-name: Children
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          description: >-
            We also support '==', but we’re not exporting that to swagger,
            because it can’t deal with it add >, >=, <, <= to that list, it
            breaks codegen.
          enum:
            - and
            - or
            - not
            - eq
            - '!='
            - ne
            - exists
            - not-exists
            - gt
            - gte
            - lt
            - lte
            - starts-with
            - not-starts-with
            - ends-with
            - not-ends-with
            - contains
            - not-contains
            - regexp
            - not-regexp
          x-go-name: Op
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Filter
    GroupInfo:
      title: >-
        GroupInfo captures information about a grouping clause in the tabular
        result format. See Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: GroupInfo
    Interval:
      required:
        - endTime
        - startTime
      type: object
      properties:
        endTime:
          type: string
          format: date-time
          x-go-name: EndTime
        groups:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Groups
        startTime:
          type: string
          format: date-time
          x-go-name: StartTime
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Interval
    Message:
      required:
        - count
        - msg
        - priority
      type: object
      properties:
        code:
          type: string
          x-go-name: Code
        count:
          type: integer
          format: int64
          x-go-name: Count
        msg:
          type: string
          x-go-name: Msg
        priority:
          type: string
          x-go-name: Priority
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Message
    Order:
      required:
        - desc
        - field
      type: object
      properties:
        desc:
          type: boolean
          x-go-name: Desc
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Order
    Projection:
      required:
        - field
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Projection
    QueryOptions:
      type: object
      properties:
        against:
          type: string
        againstStart:
          type: string
        againstTimestamp:
          type: string
        aggChartOpts:
          type: string
        caseSensitive:
          type: string
        containsTimeFilter:
          type: string
        datasets:
          type: string
        displayNull:
          type: string
        editorContent:
          type: string
        endColumn:
          type: string
        endLineNumber:
          type: string
        endTime:
          type: string
        integrationsFilter:
          type: string
        openIntervals:
          type: string
        quickRange:
          type: string
        resolution:
          type: string
        shownColumns:
          type: string
        startColumn:
          type: string
        startLineNumber:
          type: string
        startTime:
          type: string
        timeSeriesVariant:
          type: string
        timeSeriesView:
          type: string
    QueryRequest:
      required:
        - endTime
        - resolution
        - startTime
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/Aggregation'
          x-go-name: Aggregations
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        cursor:
          type: string
          x-go-name: Cursor
        endTime:
          type: string
          x-go-name: EndTime
        fieldsMeta:
          type: array
          description: >-
            FieldsMeta contains the unit information (if we have it) for each
            field
          items:
            $ref: '#/components/schemas/DatasetField'
          x-go-name: FieldsMeta
        filter:
          $ref: '#/components/schemas/Filter'
        groupBy:
          type: array
          items:
            type: string
          x-go-name: GroupBy
        includeCursor:
          type: boolean
          x-go-name: IncludeCursor
        limit:
          type: integer
          format: uint32
          x-go-name: Limit
        order:
          type: array
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        project:
          type: array
          items:
            $ref: '#/components/schemas/Projection'
          x-go-name: Project
        resolution:
          type: string
          description: >-
            The time resolution of the query’s graph, in seconds. Valid values
            are

            the query’s time range /100 at maximum and /1000 at minimum or
            "auto".
          x-go-name: Resolution
        startTime:
          type: string
          description: >-
            start and end time for the query, these must be specified as RFC3339
            strings

            or using relative time expressions (e.g. now-1h, now-1d, now-1w,
            etc)
          x-go-name: StartTime
        virtualFields:
          type: array
          items:
            $ref: '#/components/schemas/VirtualColumn'
          x-go-name: VirtualColumns
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: QueryRequest
    RangeInfo:
      required:
        - field
        - start
        - end
      title: RangeInfo specifies the window a query was restricted to.
      type: object
      properties:
        end:
          type: string
          description: |-
            End is the ending time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: End
        field:
          type: string
          description: >-
            Field specifies the field name on which the query range was
            restricted. Normally _time
          x-go-name: Field
        start:
          type: string
          description: |-
            Start is the starting time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: Start
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: RangeInfo
    SourceInfo:
      required:
        - name
      title: SourceInfo specifies the provenance of a results Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      description: >-
        Result sources will typically be the names of a datasets that were
        searched,

        but may be expanded to other things in the future.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: SourceInfo
    Status:
      required:
        - blocksExamined
        - cacheStatus
        - elapsedTime
        - isPartial
        - maxBlockTime
        - minBlockTime
        - numGroups
        - rowsExamined
        - rowsMatched
      type: object
      properties:
        blocksExamined:
          type: integer
          format: uint64
          x-go-name: BlocksExamined
        cacheStatus:
          type: integer
          format: uint8
          x-go-name: CacheStatus
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        elapsedTime:
          type: integer
          format: int64
          x-go-name: ElapsedTime
        isEstimate:
          type: boolean
          x-go-name: IsEstimate
        isPartial:
          type: boolean
          x-go-name: IsPartial
        maxBlockTime:
          type: string
          format: date-time
          x-go-name: MaxBlockTime
        maxCursor:
          type: string
          description: >-
            Row id of the newest row, as seen server side.

            May be higher than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MaxCursor
        messages:
          type: array
          items:
            $ref: '#/components/schemas/Message'
          x-go-name: Messages
        minBlockTime:
          type: string
          format: date-time
          x-go-name: MinBlockTime
        minCursor:
          type: string
          description: >-
            Row id of the oldest row, as seen server side.

            May be lower than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MinCursor
        numGroups:
          type: integer
          format: uint32
          x-go-name: NumGroups
        rowsExamined:
          type: integer
          format: uint64
          x-go-name: RowsExamined
        rowsMatched:
          type: integer
          format: uint64
          x-go-name: RowsMatched
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Status
    Table:
      required:
        - name
        - sources
        - fields
        - order
        - groups
      title: >-
        Table defines the schema for query results in the "tabular" result
        format.
      type: object
      properties:
        buckets:
          $ref: '#/components/schemas/BucketInfo'
        columns:
          type: array
          description: |-
            Columns contain a series of arrays with the raw result data.
            The columns here line up with the fields in the Fields array.
          items:
            type: array
            items:
              type: object
              properties: {}
          x-go-name: Columns
        fields:
          type: array
          description: >-
            Fields contain information about the fields included in these
            results.

            The order of the fields match up with the order of the data in
            Columns.
          items:
            $ref: '#/components/schemas/FieldInfo'
          x-go-name: Fields
        groups:
          type: array
          description: >-
            Groups specifies which grouping operations has been performed on the
            results.
          items:
            $ref: '#/components/schemas/GroupInfo'
          x-go-name: GroupBy
        name:
          type: string
          description: >-
            Name is the name assigned to this table. Defaults to "0". The name
            "_totals" is reserved for system use.
          x-go-name: Name
        order:
          type: array
          description: Order echoes the ordering clauses that was used to sort the results.
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        range:
          $ref: '#/components/schemas/RangeInfo'
        sources:
          type: array
          description: >-
            Sources contain the names of the datasets that contributed data to
            these results.
          items:
            $ref: '#/components/schemas/SourceInfo'
          x-go-name: Sources
      description: >-
        The tabular result format can be enabled via APLQueryParams.ResultFormat
        or QueryParams.ResultFormat.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Table
    Timeseries:
      type: object
      properties:
        series:
          type: array
          items:
            $ref: '#/components/schemas/Interval'
          x-go-name: Series
        totals:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Totals
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Timeseries
    VirtualColumn:
      required:
        - alias
        - expr
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        expr:
          type: string
          x-go-name: Expr
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: VirtualColumn

````# Run query

> Query

## OpenAPI

````yaml v1 post /datasets/_apl?format=tabular
paths:
  path: /datasets/_apl?format=tabular
  method: post
  servers:
    - url: https://api.axiom.co/v1/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query:
        format:
          schema:
            - type: enum<string>
              enum:
                - legacy
                - tabular
              required: true
        nocache:
          schema:
            - type: boolean
              default: false
        saveAsKind:
          schema:
            - type: string
        dataset_name:
          schema:
            - type: string
              description: >-
                When saveAsKind is true, this parameter indicates the name of
                the associated dataset.
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              apl:
                allOf:
                  - type: string
              cursor:
                allOf:
                  - type: string
              endTime:
                allOf:
                  - type: string
              includeCursor:
                allOf:
                  - type: boolean
              queryOptions:
                allOf:
                  - $ref: '#/components/schemas/QueryOptions'
              startTime:
                allOf:
                  - type: string
                    description: >-
                      start and end time for the query, these must be specified
                      as RFC3339 strings

                      or using relative time expressions (e.g. now-1h, now-1d,
                      now-1w, etc)
              variables:
                allOf:
                  - type: object
                    additionalProperties:
                      type: object
                      properties: {}
                    description: >-
                      Variables is an optional set of additional variables that
                      are inserted into the APL
            required: true
            refIdentifier: '#/components/schemas/APLRequestWithOptions'
            requiredProperties:
              - apl
            example:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
        examples:
          example:
            value:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              buckets:
                allOf:
                  - $ref: '#/components/schemas/Timeseries'
              datasetNames:
                allOf:
                  - type: array
                    items:
                      type: string
                    x-go-name: DatasetNames
              fieldsMetaMap:
                allOf:
                  - type: object
                    additionalProperties:
                      type: array
                      items:
                        $ref: '#/components/schemas/DatasetField'
                    description: >-
                      FieldsMetaMap contains the unit information (if we have
                      it) for each field in the given dataset entry
                    x-go-name: FieldsMetaMap
              format:
                allOf:
                  - type: string
                    description: >-
                      Format specifies the result set format. Either "legacy"
                      (default) or "tabular".
                    x-go-name: Format
              matches:
                allOf:
                  - type: array
                    description: >-
                      Matches hold the matching events of a filter query in the
                      "legacy" result format
                    items:
                      $ref: '#/components/schemas/Entry'
                    x-go-name: Matches
              request:
                allOf:
                  - $ref: '#/components/schemas/QueryRequest'
              status:
                allOf:
                  - $ref: '#/components/schemas/Status'
              tables:
                allOf:
                  - type: array
                    description: >-
                      Tables hold the result tables in the "tabular" result
                      format
                    items:
                      $ref: '#/components/schemas/Table'
                    x-go-name: Tables
            refIdentifier: '#/components/schemas/AplResult'
            requiredProperties:
              - datasetNames
              - format
              - status
            example:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        examples:
          example:
            value:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        description: Successful APL result
    '403':
      application/json:
        schemaArray:
          - type: object
            properties:
              code:
                allOf:
                  - type: string
              message:
                allOf:
                  - type: string
            refIdentifier: '#/components/schemas/ForbiddenError'
            example:
              code: 403
              message: Forbidden
        examples:
          example:
            value:
              code: 403
              message: Forbidden
        description: Forbidden
  deprecated: false
  type: path
components:
  schemas:
    AggInfo:
      required:
        - name
      type: object
      properties:
        args:
          type: array
          description: >-
            Args specifies any non-field arguments for the aggregation. Fx. [10]
            for topk(players, 10).
          items:
            type: object
            properties: {}
          x-go-name: Args
        fields:
          type: array
          description: >-
            Fields specifies the names of the fields this aggregation is
            computed on.

            Fx ["players"] for topk(players, 10)
          items:
            type: string
          x-go-name: Fields
        name:
          type: string
          description: >-
            Name is the system name of the aggregation, which is the string form
            of aggregation.Type.

            If the aggregation is aliased, the alias is stored in the parent
            FieldInfo
          x-go-name: Name
      description: AggInfo captures information about an aggregation
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: AggInfo
    Aggregation:
      required:
        - field
        - op
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        argument:
          type: object
          properties: {}
          x-go-name: Argument
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          enum:
            - count
            - distinct
            - sum
            - avg
            - min
            - max
            - topk
            - percentiles
            - histogram
            - stdev
            - variance
            - argmin
            - argmax
            - makeset
            - rate
            - makelist
          x-go-name: Op
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Aggregation
    BucketInfo:
      required:
        - field
        - size
      title: >-
        BucketInfo captures information about how a grouped query is sorted into
        buckets.
      type: object
      properties:
        field:
          type: string
          description: >-
            Field specifies the field used to create buckets on. Normally this
            would be _time.
          x-go-name: Field
        size:
          type: object
          properties: {}
          description: |-
            An integer or float representing the fixed bucket size.
            When the bucket field is _time this value is in nanoseconds.
          x-go-name: Size
      description: The standard mode of operation is to create buckets on the _time column,
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: BucketInfo
    DatasetField:
      required:
        - hidden
        - name
        - type
        - unit
      type: object
      properties:
        description:
          type: string
          x-go-name: Description
        hidden:
          type: boolean
          x-go-name: Hidden
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
        unit:
          type: string
          x-go-name: Unit
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: DatasetField
    Entry:
      required:
        - _rowId
        - _sysTime
        - _time
        - data
      type: object
      properties:
        _rowId:
          type: string
          x-go-name: RowID
        _sysTime:
          type: string
          format: date-time
          x-go-name: SysTime
        _time:
          type: string
          format: date-time
          x-go-name: Time
        data:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Data
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Entry
    EntryGroup:
      required:
        - group
        - id
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroupAgg'
          x-go-name: Aggregations
        group:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Group
        id:
          type: integer
          format: uint64
          x-go-name: ID
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroup
    EntryGroupAgg:
      required:
        - op
        - value
      type: object
      properties:
        data:
          type: object
          properties: {}
          x-go-name: Data
        op:
          type: string
          x-go-name: Alias
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroupAgg
    FieldInfo:
      required:
        - name
        - type
      title: >-
        FieldInfo captures information about a field used in the tabular result
        format. See Table.
      type: object
      properties:
        agg:
          $ref: '#/components/schemas/AggInfo'
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: FieldInfo
    Filter:
      required:
        - field
        - op
      type: object
      properties:
        caseSensitive:
          type: boolean
          description: >-
            Supported for these filters: starts-with, not-starts-with,
            ends-with, not-ends-with, contains, not-contains, eq, ne.
          x-go-name: CaseSensitive
        children:
          type: array
          description: 'Supported for these filters: and, or, not.'
          items:
            type: string
          x-go-name: Children
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          description: >-
            We also support '==', but we’re not exporting that to swagger,
            because it can’t deal with it add >, >=, <, <= to that list, it
            breaks codegen.
          enum:
            - and
            - or
            - not
            - eq
            - '!='
            - ne
            - exists
            - not-exists
            - gt
            - gte
            - lt
            - lte
            - starts-with
            - not-starts-with
            - ends-with
            - not-ends-with
            - contains
            - not-contains
            - regexp
            - not-regexp
          x-go-name: Op
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Filter
    GroupInfo:
      title: >-
        GroupInfo captures information about a grouping clause in the tabular
        result format. See Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: GroupInfo
    Interval:
      required:
        - endTime
        - startTime
      type: object
      properties:
        endTime:
          type: string
          format: date-time
          x-go-name: EndTime
        groups:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Groups
        startTime:
          type: string
          format: date-time
          x-go-name: StartTime
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Interval
    Message:
      required:
        - count
        - msg
        - priority
      type: object
      properties:
        code:
          type: string
          x-go-name: Code
        count:
          type: integer
          format: int64
          x-go-name: Count
        msg:
          type: string
          x-go-name: Msg
        priority:
          type: string
          x-go-name: Priority
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Message
    Order:
      required:
        - desc
        - field
      type: object
      properties:
        desc:
          type: boolean
          x-go-name: Desc
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Order
    Projection:
      required:
        - field
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Projection
    QueryOptions:
      type: object
      properties:
        against:
          type: string
        againstStart:
          type: string
        againstTimestamp:
          type: string
        aggChartOpts:
          type: string
        caseSensitive:
          type: string
        containsTimeFilter:
          type: string
        datasets:
          type: string
        displayNull:
          type: string
        editorContent:
          type: string
        endColumn:
          type: string
        endLineNumber:
          type: string
        endTime:
          type: string
        integrationsFilter:
          type: string
        openIntervals:
          type: string
        quickRange:
          type: string
        resolution:
          type: string
        shownColumns:
          type: string
        startColumn:
          type: string
        startLineNumber:
          type: string
        startTime:
          type: string
        timeSeriesVariant:
          type: string
        timeSeriesView:
          type: string
    QueryRequest:
      required:
        - endTime
        - resolution
        - startTime
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/Aggregation'
          x-go-name: Aggregations
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        cursor:
          type: string
          x-go-name: Cursor
        endTime:
          type: string
          x-go-name: EndTime
        fieldsMeta:
          type: array
          description: >-
            FieldsMeta contains the unit information (if we have it) for each
            field
          items:
            $ref: '#/components/schemas/DatasetField'
          x-go-name: FieldsMeta
        filter:
          $ref: '#/components/schemas/Filter'
        groupBy:
          type: array
          items:
            type: string
          x-go-name: GroupBy
        includeCursor:
          type: boolean
          x-go-name: IncludeCursor
        limit:
          type: integer
          format: uint32
          x-go-name: Limit
        order:
          type: array
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        project:
          type: array
          items:
            $ref: '#/components/schemas/Projection'
          x-go-name: Project
        resolution:
          type: string
          description: >-
            The time resolution of the query’s graph, in seconds. Valid values
            are

            the query’s time range /100 at maximum and /1000 at minimum or
            "auto".
          x-go-name: Resolution
        startTime:
          type: string
          description: >-
            start and end time for the query, these must be specified as RFC3339
            strings

            or using relative time expressions (e.g. now-1h, now-1d, now-1w,
            etc)
          x-go-name: StartTime
        virtualFields:
          type: array
          items:
            $ref: '#/components/schemas/VirtualColumn'
          x-go-name: VirtualColumns
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: QueryRequest
    RangeInfo:
      required:
        - field
        - start
        - end
      title: RangeInfo specifies the window a query was restricted to.
      type: object
      properties:
        end:
          type: string
          description: |-
            End is the ending time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: End
        field:
          type: string
          description: >-
            Field specifies the field name on which the query range was
            restricted. Normally _time
          x-go-name: Field
        start:
          type: string
          description: |-
            Start is the starting time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: Start
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: RangeInfo
    SourceInfo:
      required:
        - name
      title: SourceInfo specifies the provenance of a results Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      description: >-
        Result sources will typically be the names of a datasets that were
        searched,

        but may be expanded to other things in the future.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: SourceInfo
    Status:
      required:
        - blocksExamined
        - cacheStatus
        - elapsedTime
        - isPartial
        - maxBlockTime
        - minBlockTime
        - numGroups
        - rowsExamined
        - rowsMatched
      type: object
      properties:
        blocksExamined:
          type: integer
          format: uint64
          x-go-name: BlocksExamined
        cacheStatus:
          type: integer
          format: uint8
          x-go-name: CacheStatus
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        elapsedTime:
          type: integer
          format: int64
          x-go-name: ElapsedTime
        isEstimate:
          type: boolean
          x-go-name: IsEstimate
        isPartial:
          type: boolean
          x-go-name: IsPartial
        maxBlockTime:
          type: string
          format: date-time
          x-go-name: MaxBlockTime
        maxCursor:
          type: string
          description: >-
            Row id of the newest row, as seen server side.

            May be higher than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MaxCursor
        messages:
          type: array
          items:
            $ref: '#/components/schemas/Message'
          x-go-name: Messages
        minBlockTime:
          type: string
          format: date-time
          x-go-name: MinBlockTime
        minCursor:
          type: string
          description: >-
            Row id of the oldest row, as seen server side.

            May be lower than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MinCursor
        numGroups:
          type: integer
          format: uint32
          x-go-name: NumGroups
        rowsExamined:
          type: integer
          format: uint64
          x-go-name: RowsExamined
        rowsMatched:
          type: integer
          format: uint64
          x-go-name: RowsMatched
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Status
    Table:
      required:
        - name
        - sources
        - fields
        - order
        - groups
      title: >-
        Table defines the schema for query results in the "tabular" result
        format.
      type: object
      properties:
        buckets:
          $ref: '#/components/schemas/BucketInfo'
        columns:
          type: array
          description: |-
            Columns contain a series of arrays with the raw result data.
            The columns here line up with the fields in the Fields array.
          items:
            type: array
            items:
              type: object
              properties: {}
          x-go-name: Columns
        fields:
          type: array
          description: >-
            Fields contain information about the fields included in these
            results.

            The order of the fields match up with the order of the data in
            Columns.
          items:
            $ref: '#/components/schemas/FieldInfo'
          x-go-name: Fields
        groups:
          type: array
          description: >-
            Groups specifies which grouping operations has been performed on the
            results.
          items:
            $ref: '#/components/schemas/GroupInfo'
          x-go-name: GroupBy
        name:
          type: string
          description: >-
            Name is the name assigned to this table. Defaults to "0". The name
            "_totals" is reserved for system use.
          x-go-name: Name
        order:
          type: array
          description: Order echoes the ordering clauses that was used to sort the results.
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        range:
          $ref: '#/components/schemas/RangeInfo'
        sources:
          type: array
          description: >-
            Sources contain the names of the datasets that contributed data to
            these results.
          items:
            $ref: '#/components/schemas/SourceInfo'
          x-go-name: Sources
      description: >-
        The tabular result format can be enabled via APLQueryParams.ResultFormat
        or QueryParams.ResultFormat.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Table
    Timeseries:
      type: object
      properties:
        series:
          type: array
          items:
            $ref: '#/components/schemas/Interval'
          x-go-name: Series
        totals:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Totals
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Timeseries
    VirtualColumn:
      required:
        - alias
        - expr
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        expr:
          type: string
          x-go-name: Expr
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: VirtualColumn

```# Run query

> Query

## OpenAPI

````yaml v1 post /datasets/_apl?format=tabular
paths:
  path: /datasets/_apl?format=tabular
  method: post
  servers:
    - url: https://api.axiom.co/v1/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query:
        format:
          schema:
            - type: enum<string>
              enum:
                - legacy
                - tabular
              required: true
        nocache:
          schema:
            - type: boolean
              default: false
        saveAsKind:
          schema:
            - type: string
        dataset_name:
          schema:
            - type: string
              description: >-
                When saveAsKind is true, this parameter indicates the name of
                the associated dataset.
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              apl:
                allOf:
                  - type: string
              cursor:
                allOf:
                  - type: string
              endTime:
                allOf:
                  - type: string
              includeCursor:
                allOf:
                  - type: boolean
              queryOptions:
                allOf:
                  - $ref: '#/components/schemas/QueryOptions'
              startTime:
                allOf:
                  - type: string
                    description: >-
                      start and end time for the query, these must be specified
                      as RFC3339 strings

                      or using relative time expressions (e.g. now-1h, now-1d,
                      now-1w, etc)
              variables:
                allOf:
                  - type: object
                    additionalProperties:
                      type: object
                      properties: {}
                    description: >-
                      Variables is an optional set of additional variables that
                      are inserted into the APL
            required: true
            refIdentifier: '#/components/schemas/APLRequestWithOptions'
            requiredProperties:
              - apl
            example:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
        examples:
          example:
            value:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              buckets:
                allOf:
                  - $ref: '#/components/schemas/Timeseries'
              datasetNames:
                allOf:
                  - type: array
                    items:
                      type: string
                    x-go-name: DatasetNames
              fieldsMetaMap:
                allOf:
                  - type: object
                    additionalProperties:
                      type: array
                      items:
                        $ref: '#/components/schemas/DatasetField'
                    description: >-
                      FieldsMetaMap contains the unit information (if we have
                      it) for each field in the given dataset entry
                    x-go-name: FieldsMetaMap
              format:
                allOf:
                  - type: string
                    description: >-
                      Format specifies the result set format. Either "legacy"
                      (default) or "tabular".
                    x-go-name: Format
              matches:
                allOf:
                  - type: array
                    description: >-
                      Matches hold the matching events of a filter query in the
                      "legacy" result format
                    items:
                      $ref: '#/components/schemas/Entry'
                    x-go-name: Matches
              request:
                allOf:
                  - $ref: '#/components/schemas/QueryRequest'
              status:
                allOf:
                  - $ref: '#/components/schemas/Status'
              tables:
                allOf:
                  - type: array
                    description: >-
                      Tables hold the result tables in the "tabular" result
                      format
                    items:
                      $ref: '#/components/schemas/Table'
                    x-go-name: Tables
            refIdentifier: '#/components/schemas/AplResult'
            requiredProperties:
              - datasetNames
              - format
              - status
            example:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        examples:
          example:
            value:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        description: Successful APL result
    '403':
      application/json:
        schemaArray:
          - type: object
            properties:
              code:
                allOf:
                  - type: string
              message:
                allOf:
                  - type: string
            refIdentifier: '#/components/schemas/ForbiddenError'
            example:
              code: 403
              message: Forbidden
        examples:
          example:
            value:
              code: 403
              message: Forbidden
        description: Forbidden
  deprecated: false
  type: path
components:
  schemas:
    AggInfo:
      required:
        - name
      type: object
      properties:
        args:
          type: array
          description: >-
            Args specifies any non-field arguments for the aggregation. Fx. [10]
            for topk(players, 10).
          items:
            type: object
            properties: {}
          x-go-name: Args
        fields:
          type: array
          description: >-
            Fields specifies the names of the fields this aggregation is
            computed on.

            Fx ["players"] for topk(players, 10)
          items:
            type: string
          x-go-name: Fields
        name:
          type: string
          description: >-
            Name is the system name of the aggregation, which is the string form
            of aggregation.Type.

            If the aggregation is aliased, the alias is stored in the parent
            FieldInfo
          x-go-name: Name
      description: AggInfo captures information about an aggregation
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: AggInfo
    Aggregation:
      required:
        - field
        - op
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        argument:
          type: object
          properties: {}
          x-go-name: Argument
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          enum:
            - count
            - distinct
            - sum
            - avg
            - min
            - max
            - topk
            - percentiles
            - histogram
            - stdev
            - variance
            - argmin
            - argmax
            - makeset
            - rate
            - makelist
          x-go-name: Op
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Aggregation
    BucketInfo:
      required:
        - field
        - size
      title: >-
        BucketInfo captures information about how a grouped query is sorted into
        buckets.
      type: object
      properties:
        field:
          type: string
          description: >-
            Field specifies the field used to create buckets on. Normally this
            would be _time.
          x-go-name: Field
        size:
          type: object
          properties: {}
          description: |-
            An integer or float representing the fixed bucket size.
            When the bucket field is _time this value is in nanoseconds.
          x-go-name: Size
      description: The standard mode of operation is to create buckets on the _time column,
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: BucketInfo
    DatasetField:
      required:
        - hidden
        - name
        - type
        - unit
      type: object
      properties:
        description:
          type: string
          x-go-name: Description
        hidden:
          type: boolean
          x-go-name: Hidden
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
        unit:
          type: string
          x-go-name: Unit
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: DatasetField
    Entry:
      required:
        - _rowId
        - _sysTime
        - _time
        - data
      type: object
      properties:
        _rowId:
          type: string
          x-go-name: RowID
        _sysTime:
          type: string
          format: date-time
          x-go-name: SysTime
        _time:
          type: string
          format: date-time
          x-go-name: Time
        data:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Data
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Entry
    EntryGroup:
      required:
        - group
        - id
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroupAgg'
          x-go-name: Aggregations
        group:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Group
        id:
          type: integer
          format: uint64
          x-go-name: ID
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroup
    EntryGroupAgg:
      required:
        - op
        - value
      type: object
      properties:
        data:
          type: object
          properties: {}
          x-go-name: Data
        op:
          type: string
          x-go-name: Alias
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroupAgg
    FieldInfo:
      required:
        - name
        - type
      title: >-
        FieldInfo captures information about a field used in the tabular result
        format. See Table.
      type: object
      properties:
        agg:
          $ref: '#/components/schemas/AggInfo'
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: FieldInfo
    Filter:
      required:
        - field
        - op
      type: object
      properties:
        caseSensitive:
          type: boolean
          description: >-
            Supported for these filters: starts-with, not-starts-with,
            ends-with, not-ends-with, contains, not-contains, eq, ne.
          x-go-name: CaseSensitive
        children:
          type: array
          description: 'Supported for these filters: and, or, not.'
          items:
            type: string
          x-go-name: Children
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          description: >-
            We also support '==', but we’re not exporting that to swagger,
            because it can’t deal with it add >, >=, <, <= to that list, it
            breaks codegen.
          enum:
            - and
            - or
            - not
            - eq
            - '!='
            - ne
            - exists
            - not-exists
            - gt
            - gte
            - lt
            - lte
            - starts-with
            - not-starts-with
            - ends-with
            - not-ends-with
            - contains
            - not-contains
            - regexp
            - not-regexp
          x-go-name: Op
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Filter
    GroupInfo:
      title: >-
        GroupInfo captures information about a grouping clause in the tabular
        result format. See Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: GroupInfo
    Interval:
      required:
        - endTime
        - startTime
      type: object
      properties:
        endTime:
          type: string
          format: date-time
          x-go-name: EndTime
        groups:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Groups
        startTime:
          type: string
          format: date-time
          x-go-name: StartTime
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Interval
    Message:
      required:
        - count
        - msg
        - priority
      type: object
      properties:
        code:
          type: string
          x-go-name: Code
        count:
          type: integer
          format: int64
          x-go-name: Count
        msg:
          type: string
          x-go-name: Msg
        priority:
          type: string
          x-go-name: Priority
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Message
    Order:
      required:
        - desc
        - field
      type: object
      properties:
        desc:
          type: boolean
          x-go-name: Desc
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Order
    Projection:
      required:
        - field
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Projection
    QueryOptions:
      type: object
      properties:
        against:
          type: string
        againstStart:
          type: string
        againstTimestamp:
          type: string
        aggChartOpts:
          type: string
        caseSensitive:
          type: string
        containsTimeFilter:
          type: string
        datasets:
          type: string
        displayNull:
          type: string
        editorContent:
          type: string
        endColumn:
          type: string
        endLineNumber:
          type: string
        endTime:
          type: string
        integrationsFilter:
          type: string
        openIntervals:
          type: string
        quickRange:
          type: string
        resolution:
          type: string
        shownColumns:
          type: string
        startColumn:
          type: string
        startLineNumber:
          type: string
        startTime:
          type: string
        timeSeriesVariant:
          type: string
        timeSeriesView:
          type: string
    QueryRequest:
      required:
        - endTime
        - resolution
        - startTime
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/Aggregation'
          x-go-name: Aggregations
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        cursor:
          type: string
          x-go-name: Cursor
        endTime:
          type: string
          x-go-name: EndTime
        fieldsMeta:
          type: array
          description: >-
            FieldsMeta contains the unit information (if we have it) for each
            field
          items:
            $ref: '#/components/schemas/DatasetField'
          x-go-name: FieldsMeta
        filter:
          $ref: '#/components/schemas/Filter'
        groupBy:
          type: array
          items:
            type: string
          x-go-name: GroupBy
        includeCursor:
          type: boolean
          x-go-name: IncludeCursor
        limit:
          type: integer
          format: uint32
          x-go-name: Limit
        order:
          type: array
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        project:
          type: array
          items:
            $ref: '#/components/schemas/Projection'
          x-go-name: Project
        resolution:
          type: string
          description: >-
            The time resolution of the query’s graph, in seconds. Valid values
            are

            the query’s time range /100 at maximum and /1000 at minimum or
            "auto".
          x-go-name: Resolution
        startTime:
          type: string
          description: >-
            start and end time for the query, these must be specified as RFC3339
            strings

            or using relative time expressions (e.g. now-1h, now-1d, now-1w,
            etc)
          x-go-name: StartTime
        virtualFields:
          type: array
          items:
            $ref: '#/components/schemas/VirtualColumn'
          x-go-name: VirtualColumns
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: QueryRequest
    RangeInfo:
      required:
        - field
        - start
        - end
      title: RangeInfo specifies the window a query was restricted to.
      type: object
      properties:
        end:
          type: string
          description: |-
            End is the ending time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: End
        field:
          type: string
          description: >-
            Field specifies the field name on which the query range was
            restricted. Normally _time
          x-go-name: Field
        start:
          type: string
          description: |-
            Start is the starting time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: Start
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: RangeInfo
    SourceInfo:
      required:
        - name
      title: SourceInfo specifies the provenance of a results Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      description: >-
        Result sources will typically be the names of a datasets that were
        searched,

        but may be expanded to other things in the future.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: SourceInfo
    Status:
      required:
        - blocksExamined
        - cacheStatus
        - elapsedTime
        - isPartial
        - maxBlockTime
        - minBlockTime
        - numGroups
        - rowsExamined
        - rowsMatched
      type: object
      properties:
        blocksExamined:
          type: integer
          format: uint64
          x-go-name: BlocksExamined
        cacheStatus:
          type: integer
          format: uint8
          x-go-name: CacheStatus
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        elapsedTime:
          type: integer
          format: int64
          x-go-name: ElapsedTime
        isEstimate:
          type: boolean
          x-go-name: IsEstimate
        isPartial:
          type: boolean
          x-go-name: IsPartial
        maxBlockTime:
          type: string
          format: date-time
          x-go-name: MaxBlockTime
        maxCursor:
          type: string
          description: >-
            Row id of the newest row, as seen server side.

            May be higher than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MaxCursor
        messages:
          type: array
          items:
            $ref: '#/components/schemas/Message'
          x-go-name: Messages
        minBlockTime:
          type: string
          format: date-time
          x-go-name: MinBlockTime
        minCursor:
          type: string
          description: >-
            Row id of the oldest row, as seen server side.

            May be lower than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MinCursor
        numGroups:
          type: integer
          format: uint32
          x-go-name: NumGroups
        rowsExamined:
          type: integer
          format: uint64
          x-go-name: RowsExamined
        rowsMatched:
          type: integer
          format: uint64
          x-go-name: RowsMatched
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Status
    Table:
      required:
        - name
        - sources
        - fields
        - order
        - groups
      title: >-
        Table defines the schema for query results in the "tabular" result
        format.
      type: object
      properties:
        buckets:
          $ref: '#/components/schemas/BucketInfo'
        columns:
          type: array
          description: |-
            Columns contain a series of arrays with the raw result data.
            The columns here line up with the fields in the Fields array.
          items:
            type: array
            items:
              type: object
              properties: {}
          x-go-name: Columns
        fields:
          type: array
          description: >-
            Fields contain information about the fields included in these
            results.

            The order of the fields match up with the order of the data in
            Columns.
          items:
            $ref: '#/components/schemas/FieldInfo'
          x-go-name: Fields
        groups:
          type: array
          description: >-
            Groups specifies which grouping operations has been performed on the
            results.
          items:
            $ref: '#/components/schemas/GroupInfo'
          x-go-name: GroupBy
        name:
          type: string
          description: >-
            Name is the name assigned to this table. Defaults to "0". The name
            "_totals" is reserved for system use.
          x-go-name: Name
        order:
          type: array
          description: Order echoes the ordering clauses that was used to sort the results.
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        range:
          $ref: '#/components/schemas/RangeInfo'
        sources:
          type: array
          description: >-
            Sources contain the names of the datasets that contributed data to
            these results.
          items:
            $ref: '#/components/schemas/SourceInfo'
          x-go-name: Sources
      description: >-
        The tabular result format can be enabled via APLQueryParams.ResultFormat
        or QueryParams.ResultFormat.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Table
    Timeseries:
      type: object
      properties:
        series:
          type: array
          items:
            $ref: '#/components/schemas/Interval'
          x-go-name: Series
        totals:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Totals
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Timeseries
    VirtualColumn:
      required:
        - alias
        - expr
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        expr:
          type: string
          x-go-name: Expr
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: VirtualColumn

`````# Run query

> Query

## OpenAPI

````yaml v1 post /datasets/_apl?format=tabular
paths:
  path: /datasets/_apl?format=tabular
  method: post
  servers:
    - url: https://api.axiom.co/v1/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query:
        format:
          schema:
            - type: enum<string>
              enum:
                - legacy
                - tabular
              required: true
        nocache:
          schema:
            - type: boolean
              default: false
        saveAsKind:
          schema:
            - type: string
        dataset_name:
          schema:
            - type: string
              description: >-
                When saveAsKind is true, this parameter indicates the name of
                the associated dataset.
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              apl:
                allOf:
                  - type: string
              cursor:
                allOf:
                  - type: string
              endTime:
                allOf:
                  - type: string
              includeCursor:
                allOf:
                  - type: boolean
              queryOptions:
                allOf:
                  - $ref: '#/components/schemas/QueryOptions'
              startTime:
                allOf:
                  - type: string
                    description: >-
                      start and end time for the query, these must be specified
                      as RFC3339 strings

                      or using relative time expressions (e.g. now-1h, now-1d,
                      now-1w, etc)
              variables:
                allOf:
                  - type: object
                    additionalProperties:
                      type: object
                      properties: {}
                    description: >-
                      Variables is an optional set of additional variables that
                      are inserted into the APL
            required: true
            refIdentifier: '#/components/schemas/APLRequestWithOptions'
            requiredProperties:
              - apl
            example:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
        examples:
          example:
            value:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              buckets:
                allOf:
                  - $ref: '#/components/schemas/Timeseries'
              datasetNames:
                allOf:
                  - type: array
                    items:
                      type: string
                    x-go-name: DatasetNames
              fieldsMetaMap:
                allOf:
                  - type: object
                    additionalProperties:
                      type: array
                      items:
                        $ref: '#/components/schemas/DatasetField'
                    description: >-
                      FieldsMetaMap contains the unit information (if we have
                      it) for each field in the given dataset entry
                    x-go-name: FieldsMetaMap
              format:
                allOf:
                  - type: string
                    description: >-
                      Format specifies the result set format. Either "legacy"
                      (default) or "tabular".
                    x-go-name: Format
              matches:
                allOf:
                  - type: array
                    description: >-
                      Matches hold the matching events of a filter query in the
                      "legacy" result format
                    items:
                      $ref: '#/components/schemas/Entry'
                    x-go-name: Matches
              request:
                allOf:
                  - $ref: '#/components/schemas/QueryRequest'
              status:
                allOf:
                  - $ref: '#/components/schemas/Status'
              tables:
                allOf:
                  - type: array
                    description: >-
                      Tables hold the result tables in the "tabular" result
                      format
                    items:
                      $ref: '#/components/schemas/Table'
                    x-go-name: Tables
            refIdentifier: '#/components/schemas/AplResult'
            requiredProperties:
              - datasetNames
              - format
              - status
            example:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        examples:
          example:
            value:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        description: Successful APL result
    '403':
      application/json:
        schemaArray:
          - type: object
            properties:
              code:
                allOf:
                  - type: string
              message:
                allOf:
                  - type: string
            refIdentifier: '#/components/schemas/ForbiddenError'
            example:
              code: 403
              message: Forbidden
        examples:
          example:
            value:
              code: 403
              message: Forbidden
        description: Forbidden
  deprecated: false
  type: path
components:
  schemas:
    AggInfo:
      required:
        - name
      type: object
      properties:
        args:
          type: array
          description: >-
            Args specifies any non-field arguments for the aggregation. Fx. [10]
            for topk(players, 10).
          items:
            type: object
            properties: {}
          x-go-name: Args
        fields:
          type: array
          description: >-
            Fields specifies the names of the fields this aggregation is
            computed on.

            Fx ["players"] for topk(players, 10)
          items:
            type: string
          x-go-name: Fields
        name:
          type: string
          description: >-
            Name is the system name of the aggregation, which is the string form
            of aggregation.Type.

            If the aggregation is aliased, the alias is stored in the parent
            FieldInfo
          x-go-name: Name
      description: AggInfo captures information about an aggregation
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: AggInfo
    Aggregation:
      required:
        - field
        - op
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        argument:
          type: object
          properties: {}
          x-go-name: Argument
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          enum:
            - count
            - distinct
            - sum
            - avg
            - min
            - max
            - topk
            - percentiles
            - histogram
            - stdev
            - variance
            - argmin
            - argmax
            - makeset
            - rate
            - makelist
          x-go-name: Op
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Aggregation
    BucketInfo:
      required:
        - field
        - size
      title: >-
        BucketInfo captures information about how a grouped query is sorted into
        buckets.
      type: object
      properties:
        field:
          type: string
          description: >-
            Field specifies the field used to create buckets on. Normally this
            would be _time.
          x-go-name: Field
        size:
          type: object
          properties: {}
          description: |-
            An integer or float representing the fixed bucket size.
            When the bucket field is _time this value is in nanoseconds.
          x-go-name: Size
      description: The standard mode of operation is to create buckets on the _time column,
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: BucketInfo
    DatasetField:
      required:
        - hidden
        - name
        - type
        - unit
      type: object
      properties:
        description:
          type: string
          x-go-name: Description
        hidden:
          type: boolean
          x-go-name: Hidden
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
        unit:
          type: string
          x-go-name: Unit
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: DatasetField
    Entry:
      required:
        - _rowId
        - _sysTime
        - _time
        - data
      type: object
      properties:
        _rowId:
          type: string
          x-go-name: RowID
        _sysTime:
          type: string
          format: date-time
          x-go-name: SysTime
        _time:
          type: string
          format: date-time
          x-go-name: Time
        data:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Data
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Entry
    EntryGroup:
      required:
        - group
        - id
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroupAgg'
          x-go-name: Aggregations
        group:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Group
        id:
          type: integer
          format: uint64
          x-go-name: ID
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroup
    EntryGroupAgg:
      required:
        - op
        - value
      type: object
      properties:
        data:
          type: object
          properties: {}
          x-go-name: Data
        op:
          type: string
          x-go-name: Alias
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroupAgg
    FieldInfo:
      required:
        - name
        - type
      title: >-
        FieldInfo captures information about a field used in the tabular result
        format. See Table.
      type: object
      properties:
        agg:
          $ref: '#/components/schemas/AggInfo'
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: FieldInfo
    Filter:
      required:
        - field
        - op
      type: object
      properties:
        caseSensitive:
          type: boolean
          description: >-
            Supported for these filters: starts-with, not-starts-with,
            ends-with, not-ends-with, contains, not-contains, eq, ne.
          x-go-name: CaseSensitive
        children:
          type: array
          description: 'Supported for these filters: and, or, not.'
          items:
            type: string
          x-go-name: Children
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          description: >-
            We also support '==', but we’re not exporting that to swagger,
            because it can’t deal with it add >, >=, <, <= to that list, it
            breaks codegen.
          enum:
            - and
            - or
            - not
            - eq
            - '!='
            - ne
            - exists
            - not-exists
            - gt
            - gte
            - lt
            - lte
            - starts-with
            - not-starts-with
            - ends-with
            - not-ends-with
            - contains
            - not-contains
            - regexp
            - not-regexp
          x-go-name: Op
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Filter
    GroupInfo:
      title: >-
        GroupInfo captures information about a grouping clause in the tabular
        result format. See Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: GroupInfo
    Interval:
      required:
        - endTime
        - startTime
      type: object
      properties:
        endTime:
          type: string
          format: date-time
          x-go-name: EndTime
        groups:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Groups
        startTime:
          type: string
          format: date-time
          x-go-name: StartTime
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Interval
    Message:
      required:
        - count
        - msg
        - priority
      type: object
      properties:
        code:
          type: string
          x-go-name: Code
        count:
          type: integer
          format: int64
          x-go-name: Count
        msg:
          type: string
          x-go-name: Msg
        priority:
          type: string
          x-go-name: Priority
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Message
    Order:
      required:
        - desc
        - field
      type: object
      properties:
        desc:
          type: boolean
          x-go-name: Desc
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Order
    Projection:
      required:
        - field
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Projection
    QueryOptions:
      type: object
      properties:
        against:
          type: string
        againstStart:
          type: string
        againstTimestamp:
          type: string
        aggChartOpts:
          type: string
        caseSensitive:
          type: string
        containsTimeFilter:
          type: string
        datasets:
          type: string
        displayNull:
          type: string
        editorContent:
          type: string
        endColumn:
          type: string
        endLineNumber:
          type: string
        endTime:
          type: string
        integrationsFilter:
          type: string
        openIntervals:
          type: string
        quickRange:
          type: string
        resolution:
          type: string
        shownColumns:
          type: string
        startColumn:
          type: string
        startLineNumber:
          type: string
        startTime:
          type: string
        timeSeriesVariant:
          type: string
        timeSeriesView:
          type: string
    QueryRequest:
      required:
        - endTime
        - resolution
        - startTime
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/Aggregation'
          x-go-name: Aggregations
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        cursor:
          type: string
          x-go-name: Cursor
        endTime:
          type: string
          x-go-name: EndTime
        fieldsMeta:
          type: array
          description: >-
            FieldsMeta contains the unit information (if we have it) for each
            field
          items:
            $ref: '#/components/schemas/DatasetField'
          x-go-name: FieldsMeta
        filter:
          $ref: '#/components/schemas/Filter'
        groupBy:
          type: array
          items:
            type: string
          x-go-name: GroupBy
        includeCursor:
          type: boolean
          x-go-name: IncludeCursor
        limit:
          type: integer
          format: uint32
          x-go-name: Limit
        order:
          type: array
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        project:
          type: array
          items:
            $ref: '#/components/schemas/Projection'
          x-go-name: Project
        resolution:
          type: string
          description: >-
            The time resolution of the query’s graph, in seconds. Valid values
            are

            the query’s time range /100 at maximum and /1000 at minimum or
            "auto".
          x-go-name: Resolution
        startTime:
          type: string
          description: >-
            start and end time for the query, these must be specified as RFC3339
            strings

            or using relative time expressions (e.g. now-1h, now-1d, now-1w,
            etc)
          x-go-name: StartTime
        virtualFields:
          type: array
          items:
            $ref: '#/components/schemas/VirtualColumn'
          x-go-name: VirtualColumns
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: QueryRequest
    RangeInfo:
      required:
        - field
        - start
        - end
      title: RangeInfo specifies the window a query was restricted to.
      type: object
      properties:
        end:
          type: string
          description: |-
            End is the ending time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: End
        field:
          type: string
          description: >-
            Field specifies the field name on which the query range was
            restricted. Normally _time
          x-go-name: Field
        start:
          type: string
          description: |-
            Start is the starting time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: Start
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: RangeInfo
    SourceInfo:
      required:
        - name
      title: SourceInfo specifies the provenance of a results Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      description: >-
        Result sources will typically be the names of a datasets that were
        searched,

        but may be expanded to other things in the future.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: SourceInfo
    Status:
      required:
        - blocksExamined
        - cacheStatus
        - elapsedTime
        - isPartial
        - maxBlockTime
        - minBlockTime
        - numGroups
        - rowsExamined
        - rowsMatched
      type: object
      properties:
        blocksExamined:
          type: integer
          format: uint64
          x-go-name: BlocksExamined
        cacheStatus:
          type: integer
          format: uint8
          x-go-name: CacheStatus
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        elapsedTime:
          type: integer
          format: int64
          x-go-name: ElapsedTime
        isEstimate:
          type: boolean
          x-go-name: IsEstimate
        isPartial:
          type: boolean
          x-go-name: IsPartial
        maxBlockTime:
          type: string
          format: date-time
          x-go-name: MaxBlockTime
        maxCursor:
          type: string
          description: >-
            Row id of the newest row, as seen server side.

            May be higher than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MaxCursor
        messages:
          type: array
          items:
            $ref: '#/components/schemas/Message'
          x-go-name: Messages
        minBlockTime:
          type: string
          format: date-time
          x-go-name: MinBlockTime
        minCursor:
          type: string
          description: >-
            Row id of the oldest row, as seen server side.

            May be lower than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MinCursor
        numGroups:
          type: integer
          format: uint32
          x-go-name: NumGroups
        rowsExamined:
          type: integer
          format: uint64
          x-go-name: RowsExamined
        rowsMatched:
          type: integer
          format: uint64
          x-go-name: RowsMatched
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Status
    Table:
      required:
        - name
        - sources
        - fields
        - order
        - groups
      title: >-
        Table defines the schema for query results in the "tabular" result
        format.
      type: object
      properties:
        buckets:
          $ref: '#/components/schemas/BucketInfo'
        columns:
          type: array
          description: |-
            Columns contain a series of arrays with the raw result data.
            The columns here line up with the fields in the Fields array.
          items:
            type: array
            items:
              type: object
              properties: {}
          x-go-name: Columns
        fields:
          type: array
          description: >-
            Fields contain information about the fields included in these
            results.

            The order of the fields match up with the order of the data in
            Columns.
          items:
            $ref: '#/components/schemas/FieldInfo'
          x-go-name: Fields
        groups:
          type: array
          description: >-
            Groups specifies which grouping operations has been performed on the
            results.
          items:
            $ref: '#/components/schemas/GroupInfo'
          x-go-name: GroupBy
        name:
          type: string
          description: >-
            Name is the name assigned to this table. Defaults to "0". The name
            "_totals" is reserved for system use.
          x-go-name: Name
        order:
          type: array
          description: Order echoes the ordering clauses that was used to sort the results.
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        range:
          $ref: '#/components/schemas/RangeInfo'
        sources:
          type: array
          description: >-
            Sources contain the names of the datasets that contributed data to
            these results.
          items:
            $ref: '#/components/schemas/SourceInfo'
          x-go-name: Sources
      description: >-
        The tabular result format can be enabled via APLQueryParams.ResultFormat
        or QueryParams.ResultFormat.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Table
    Timeseries:
      type: object
      properties:
        series:
          type: array
          items:
            $ref: '#/components/schemas/Interval'
          x-go-name: Series
        totals:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Totals
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Timeseries
    VirtualColumn:
      required:
        - alias
        - expr
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        expr:
          type: string
          x-go-name: Expr
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: VirtualColumn

````# Run query

> Query

## OpenAPI

````yaml v1 post /datasets/_apl?format=tabular
paths:
  path: /datasets/_apl?format=tabular
  method: post
  servers:
    - url: https://api.axiom.co/v1/
  request:
    security:
      - title: Auth
        parameters:
          query: {}
          header:
            Authorization:
              type: oauth2
          cookie: {}
    parameters:
      path: {}
      query:
        format:
          schema:
            - type: enum<string>
              enum:
                - legacy
                - tabular
              required: true
        nocache:
          schema:
            - type: boolean
              default: false
        saveAsKind:
          schema:
            - type: string
        dataset_name:
          schema:
            - type: string
              description: >-
                When saveAsKind is true, this parameter indicates the name of
                the associated dataset.
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              apl:
                allOf:
                  - type: string
              cursor:
                allOf:
                  - type: string
              endTime:
                allOf:
                  - type: string
              includeCursor:
                allOf:
                  - type: boolean
              queryOptions:
                allOf:
                  - $ref: '#/components/schemas/QueryOptions'
              startTime:
                allOf:
                  - type: string
                    description: >-
                      start and end time for the query, these must be specified
                      as RFC3339 strings

                      or using relative time expressions (e.g. now-1h, now-1d,
                      now-1w, etc)
              variables:
                allOf:
                  - type: object
                    additionalProperties:
                      type: object
                      properties: {}
                    description: >-
                      Variables is an optional set of additional variables that
                      are inserted into the APL
            required: true
            refIdentifier: '#/components/schemas/APLRequestWithOptions'
            requiredProperties:
              - apl
            example:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
        examples:
          example:
            value:
              apl: http-logs | limit 10
              startTime: string
              endTime: string
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              buckets:
                allOf:
                  - $ref: '#/components/schemas/Timeseries'
              datasetNames:
                allOf:
                  - type: array
                    items:
                      type: string
                    x-go-name: DatasetNames
              fieldsMetaMap:
                allOf:
                  - type: object
                    additionalProperties:
                      type: array
                      items:
                        $ref: '#/components/schemas/DatasetField'
                    description: >-
                      FieldsMetaMap contains the unit information (if we have
                      it) for each field in the given dataset entry
                    x-go-name: FieldsMetaMap
              format:
                allOf:
                  - type: string
                    description: >-
                      Format specifies the result set format. Either "legacy"
                      (default) or "tabular".
                    x-go-name: Format
              matches:
                allOf:
                  - type: array
                    description: >-
                      Matches hold the matching events of a filter query in the
                      "legacy" result format
                    items:
                      $ref: '#/components/schemas/Entry'
                    x-go-name: Matches
              request:
                allOf:
                  - $ref: '#/components/schemas/QueryRequest'
              status:
                allOf:
                  - $ref: '#/components/schemas/Status'
              tables:
                allOf:
                  - type: array
                    description: >-
                      Tables hold the result tables in the "tabular" result
                      format
                    items:
                      $ref: '#/components/schemas/Table'
                    x-go-name: Tables
            refIdentifier: '#/components/schemas/AplResult'
            requiredProperties:
              - datasetNames
              - format
              - status
            example:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        examples:
          example:
            value:
              format: tabular
              status:
                elapsedTime: 260650
                minCursor: 0d8q6stroluyo-07c3957e7400015c-0000c875
                maxCursor: 0d8q6stroluyo-07c3957e7400015c-0000c877
                blocksExamined: 4
                blocksCached: 0
                blocksMatched: 0
                rowsExamined: 197604
                rowsMatched: 197604
                numGroups: 0
                isPartial: false
                cacheStatus: 1
                minBlockTime: '2025-03-26T12:03:14Z'
                maxBlockTime: '2025-03-26T12:12:42Z'
              tables:
                - name: '0'
                  sources:
                    - name: http-logs
                  fields:
                    - name: _sysTime
                      type: datetime
                    - name: _time
                      type: datetime
                    - name: content_type
                      type: string
                    - name: geo.city
                      type: string
                    - name: geo.country
                      type: string
                    - name: id
                      type: string
                    - name: is_tls
                      type: boolean
                    - name: message
                      type: string
                    - name: method
                      type: string
                    - name: req_duration_ms
                      type: float
                    - name: resp_body_size_bytes
                      type: integer
                    - name: resp_header_size_bytes
                      type: integer
                    - name: server_datacenter
                      type: string
                    - name: status
                      type: string
                    - name: uri
                      type: string
                    - name: user_agent
                      type: string
                    - name: 'is_ok_2    '
                      type: boolean
                    - name: city_str_len
                      type: integer
                  order:
                    - field: _time
                      desc: true
                  groups: []
                  range:
                    field: _time
                    start: '1970-01-01T00:00:00Z'
                    end: '2025-03-26T12:12:43Z'
                  columns:
                    - - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                      - '2025-03-26T12:12:42.68112905Z'
                    - - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                      - '2025-03-26T12:12:42Z'
                    - - text/html
                      - text/plain-charset=utf-8
                      - image/jpeg
                    - - Ojinaga
                      - Humboldt
                      - Nevers
                    - - Mexico
                      - United States
                      - France
                    - - 8af366cf-6f25-42e6-bbb4-d860ab535a60
                      - 032e7f68-b0ab-47c0-a24a-35af566359e5
                      - 4d2c7baa-ff28-4b1f-9db9-8e6c0ed5a9c9
                    - - false
                      - false
                      - true
                    - - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        QCD permutations were not solvable in linear time,
                        expected compressed time
                      - >-
                        Expected a new layer of particle physics but got a Higgs
                        Boson
                    - - GET
                      - GET
                      - GET
                    - - 1.396373193863436
                      - 0.16252390534308514
                      - 0.4093416175186162
                    - - 3448
                      - 2533
                      - 1906
                    - - 84
                      - 31
                      - 29
                    - - DCA
                      - GRU
                      - FRA
                    - - '201'
                      - '200'
                      - '200'
                    - - /api/v1/buy/commit/id/go
                      - /api/v1/textdata/cnfigs
                      - /api/v1/bank/warn
                    - - >-
                        Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS;
                        rv:11.0) like Gecko
                      - >-
                        Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24
                        (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24
                      - >-
                        Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;
                        en-US))
                    - - true
                      - true
                      - true
                    - - 7
                      - 8
                      - 6
              datasetNames:
                - http-logs
              fieldsMetaMap:
                http-logs:
                  - name: status
                    type: ''
                    unit: ''
                    hidden: false
                    description: HTTP status code
                  - name: resp_header_size_bytes
                    type: integer
                    unit: none
                    hidden: false
                    description: ''
                  - name: geo.city
                    type: string
                    unit: ''
                    hidden: false
                    description: the city
                  - name: resp_body_size_bytes
                    type: integer
                    unit: decbytes
                    hidden: false
                    description: ''
                  - name: content_type
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: geo.country
                    type: string
                    unit: ''
                    hidden: false
                    description: ''
                  - name: req_duration_ms
                    type: float
                    unit: ms
                    hidden: false
                    description: Request duration
        description: Successful APL result
    '403':
      application/json:
        schemaArray:
          - type: object
            properties:
              code:
                allOf:
                  - type: string
              message:
                allOf:
                  - type: string
            refIdentifier: '#/components/schemas/ForbiddenError'
            example:
              code: 403
              message: Forbidden
        examples:
          example:
            value:
              code: 403
              message: Forbidden
        description: Forbidden
  deprecated: false
  type: path
components:
  schemas:
    AggInfo:
      required:
        - name
      type: object
      properties:
        args:
          type: array
          description: >-
            Args specifies any non-field arguments for the aggregation. Fx. [10]
            for topk(players, 10).
          items:
            type: object
            properties: {}
          x-go-name: Args
        fields:
          type: array
          description: >-
            Fields specifies the names of the fields this aggregation is
            computed on.

            Fx ["players"] for topk(players, 10)
          items:
            type: string
          x-go-name: Fields
        name:
          type: string
          description: >-
            Name is the system name of the aggregation, which is the string form
            of aggregation.Type.

            If the aggregation is aliased, the alias is stored in the parent
            FieldInfo
          x-go-name: Name
      description: AggInfo captures information about an aggregation
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: AggInfo
    Aggregation:
      required:
        - field
        - op
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        argument:
          type: object
          properties: {}
          x-go-name: Argument
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          enum:
            - count
            - distinct
            - sum
            - avg
            - min
            - max
            - topk
            - percentiles
            - histogram
            - stdev
            - variance
            - argmin
            - argmax
            - makeset
            - rate
            - makelist
          x-go-name: Op
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Aggregation
    BucketInfo:
      required:
        - field
        - size
      title: >-
        BucketInfo captures information about how a grouped query is sorted into
        buckets.
      type: object
      properties:
        field:
          type: string
          description: >-
            Field specifies the field used to create buckets on. Normally this
            would be _time.
          x-go-name: Field
        size:
          type: object
          properties: {}
          description: |-
            An integer or float representing the fixed bucket size.
            When the bucket field is _time this value is in nanoseconds.
          x-go-name: Size
      description: The standard mode of operation is to create buckets on the _time column,
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: BucketInfo
    DatasetField:
      required:
        - hidden
        - name
        - type
        - unit
      type: object
      properties:
        description:
          type: string
          x-go-name: Description
        hidden:
          type: boolean
          x-go-name: Hidden
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
        unit:
          type: string
          x-go-name: Unit
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: DatasetField
    Entry:
      required:
        - _rowId
        - _sysTime
        - _time
        - data
      type: object
      properties:
        _rowId:
          type: string
          x-go-name: RowID
        _sysTime:
          type: string
          format: date-time
          x-go-name: SysTime
        _time:
          type: string
          format: date-time
          x-go-name: Time
        data:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Data
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Entry
    EntryGroup:
      required:
        - group
        - id
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroupAgg'
          x-go-name: Aggregations
        group:
          type: object
          additionalProperties:
            type: object
            properties: {}
          x-go-name: Group
        id:
          type: integer
          format: uint64
          x-go-name: ID
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroup
    EntryGroupAgg:
      required:
        - op
        - value
      type: object
      properties:
        data:
          type: object
          properties: {}
          x-go-name: Data
        op:
          type: string
          x-go-name: Alias
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: EntryGroupAgg
    FieldInfo:
      required:
        - name
        - type
      title: >-
        FieldInfo captures information about a field used in the tabular result
        format. See Table.
      type: object
      properties:
        agg:
          $ref: '#/components/schemas/AggInfo'
        name:
          type: string
          x-go-name: Name
        type:
          type: string
          x-go-name: Type
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: FieldInfo
    Filter:
      required:
        - field
        - op
      type: object
      properties:
        caseSensitive:
          type: boolean
          description: >-
            Supported for these filters: starts-with, not-starts-with,
            ends-with, not-ends-with, contains, not-contains, eq, ne.
          x-go-name: CaseSensitive
        children:
          type: array
          description: 'Supported for these filters: and, or, not.'
          items:
            type: string
          x-go-name: Children
        field:
          type: string
          x-go-name: Field
        op:
          type: string
          description: >-
            We also support '==', but we’re not exporting that to swagger,
            because it can’t deal with it add >, >=, <, <= to that list, it
            breaks codegen.
          enum:
            - and
            - or
            - not
            - eq
            - '!='
            - ne
            - exists
            - not-exists
            - gt
            - gte
            - lt
            - lte
            - starts-with
            - not-starts-with
            - ends-with
            - not-ends-with
            - contains
            - not-contains
            - regexp
            - not-regexp
          x-go-name: Op
        value:
          type: object
          properties: {}
          x-go-name: Value
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Filter
    GroupInfo:
      title: >-
        GroupInfo captures information about a grouping clause in the tabular
        result format. See Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: GroupInfo
    Interval:
      required:
        - endTime
        - startTime
      type: object
      properties:
        endTime:
          type: string
          format: date-time
          x-go-name: EndTime
        groups:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Groups
        startTime:
          type: string
          format: date-time
          x-go-name: StartTime
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Interval
    Message:
      required:
        - count
        - msg
        - priority
      type: object
      properties:
        code:
          type: string
          x-go-name: Code
        count:
          type: integer
          format: int64
          x-go-name: Count
        msg:
          type: string
          x-go-name: Msg
        priority:
          type: string
          x-go-name: Priority
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Message
    Order:
      required:
        - desc
        - field
      type: object
      properties:
        desc:
          type: boolean
          x-go-name: Desc
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Order
    Projection:
      required:
        - field
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        field:
          type: string
          x-go-name: Field
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Projection
    QueryOptions:
      type: object
      properties:
        against:
          type: string
        againstStart:
          type: string
        againstTimestamp:
          type: string
        aggChartOpts:
          type: string
        caseSensitive:
          type: string
        containsTimeFilter:
          type: string
        datasets:
          type: string
        displayNull:
          type: string
        editorContent:
          type: string
        endColumn:
          type: string
        endLineNumber:
          type: string
        endTime:
          type: string
        integrationsFilter:
          type: string
        openIntervals:
          type: string
        quickRange:
          type: string
        resolution:
          type: string
        shownColumns:
          type: string
        startColumn:
          type: string
        startLineNumber:
          type: string
        startTime:
          type: string
        timeSeriesVariant:
          type: string
        timeSeriesView:
          type: string
    QueryRequest:
      required:
        - endTime
        - resolution
        - startTime
      type: object
      properties:
        aggregations:
          type: array
          items:
            $ref: '#/components/schemas/Aggregation'
          x-go-name: Aggregations
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        cursor:
          type: string
          x-go-name: Cursor
        endTime:
          type: string
          x-go-name: EndTime
        fieldsMeta:
          type: array
          description: >-
            FieldsMeta contains the unit information (if we have it) for each
            field
          items:
            $ref: '#/components/schemas/DatasetField'
          x-go-name: FieldsMeta
        filter:
          $ref: '#/components/schemas/Filter'
        groupBy:
          type: array
          items:
            type: string
          x-go-name: GroupBy
        includeCursor:
          type: boolean
          x-go-name: IncludeCursor
        limit:
          type: integer
          format: uint32
          x-go-name: Limit
        order:
          type: array
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        project:
          type: array
          items:
            $ref: '#/components/schemas/Projection'
          x-go-name: Project
        resolution:
          type: string
          description: >-
            The time resolution of the query’s graph, in seconds. Valid values
            are

            the query’s time range /100 at maximum and /1000 at minimum or
            "auto".
          x-go-name: Resolution
        startTime:
          type: string
          description: >-
            start and end time for the query, these must be specified as RFC3339
            strings

            or using relative time expressions (e.g. now-1h, now-1d, now-1w,
            etc)
          x-go-name: StartTime
        virtualFields:
          type: array
          items:
            $ref: '#/components/schemas/VirtualColumn'
          x-go-name: VirtualColumns
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: QueryRequest
    RangeInfo:
      required:
        - field
        - start
        - end
      title: RangeInfo specifies the window a query was restricted to.
      type: object
      properties:
        end:
          type: string
          description: |-
            End is the ending time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: End
        field:
          type: string
          description: >-
            Field specifies the field name on which the query range was
            restricted. Normally _time
          x-go-name: Field
        start:
          type: string
          description: |-
            Start is the starting time the query is limited by.
            Queries are restricted to the interval [start,end).
          format: date-time
          x-go-name: Start
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: RangeInfo
    SourceInfo:
      required:
        - name
      title: SourceInfo specifies the provenance of a results Table.
      type: object
      properties:
        name:
          type: string
          x-go-name: Name
      description: >-
        Result sources will typically be the names of a datasets that were
        searched,

        but may be expanded to other things in the future.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: SourceInfo
    Status:
      required:
        - blocksExamined
        - cacheStatus
        - elapsedTime
        - isPartial
        - maxBlockTime
        - minBlockTime
        - numGroups
        - rowsExamined
        - rowsMatched
      type: object
      properties:
        blocksExamined:
          type: integer
          format: uint64
          x-go-name: BlocksExamined
        cacheStatus:
          type: integer
          format: uint8
          x-go-name: CacheStatus
        continuationToken:
          type: string
          x-go-name: ContinuationToken
        elapsedTime:
          type: integer
          format: int64
          x-go-name: ElapsedTime
        isEstimate:
          type: boolean
          x-go-name: IsEstimate
        isPartial:
          type: boolean
          x-go-name: IsPartial
        maxBlockTime:
          type: string
          format: date-time
          x-go-name: MaxBlockTime
        maxCursor:
          type: string
          description: >-
            Row id of the newest row, as seen server side.

            May be higher than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MaxCursor
        messages:
          type: array
          items:
            $ref: '#/components/schemas/Message'
          x-go-name: Messages
        minBlockTime:
          type: string
          format: date-time
          x-go-name: MinBlockTime
        minCursor:
          type: string
          description: >-
            Row id of the oldest row, as seen server side.

            May be lower than what the results include if the server scanned
            more data than included in the results.

            Can be used to efficiently resume time-sorted non-aggregating
            queries (ie filtering only).
          x-go-name: MinCursor
        numGroups:
          type: integer
          format: uint32
          x-go-name: NumGroups
        rowsExamined:
          type: integer
          format: uint64
          x-go-name: RowsExamined
        rowsMatched:
          type: integer
          format: uint64
          x-go-name: RowsMatched
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Status
    Table:
      required:
        - name
        - sources
        - fields
        - order
        - groups
      title: >-
        Table defines the schema for query results in the "tabular" result
        format.
      type: object
      properties:
        buckets:
          $ref: '#/components/schemas/BucketInfo'
        columns:
          type: array
          description: |-
            Columns contain a series of arrays with the raw result data.
            The columns here line up with the fields in the Fields array.
          items:
            type: array
            items:
              type: object
              properties: {}
          x-go-name: Columns
        fields:
          type: array
          description: >-
            Fields contain information about the fields included in these
            results.

            The order of the fields match up with the order of the data in
            Columns.
          items:
            $ref: '#/components/schemas/FieldInfo'
          x-go-name: Fields
        groups:
          type: array
          description: >-
            Groups specifies which grouping operations has been performed on the
            results.
          items:
            $ref: '#/components/schemas/GroupInfo'
          x-go-name: GroupBy
        name:
          type: string
          description: >-
            Name is the name assigned to this table. Defaults to "0". The name
            "_totals" is reserved for system use.
          x-go-name: Name
        order:
          type: array
          description: Order echoes the ordering clauses that was used to sort the results.
          items:
            $ref: '#/components/schemas/Order'
          x-go-name: Order
        range:
          $ref: '#/components/schemas/RangeInfo'
        sources:
          type: array
          description: >-
            Sources contain the names of the datasets that contributed data to
            these results.
          items:
            $ref: '#/components/schemas/SourceInfo'
          x-go-name: Sources
      description: >-
        The tabular result format can be enabled via APLQueryParams.ResultFormat
        or QueryParams.ResultFormat.
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Table
    Timeseries:
      type: object
      properties:
        series:
          type: array
          items:
            $ref: '#/components/schemas/Interval'
          x-go-name: Series
        totals:
          type: array
          items:
            $ref: '#/components/schemas/EntryGroup'
          x-go-name: Totals
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: Timeseries
    VirtualColumn:
      required:
        - alias
        - expr
      type: object
      properties:
        alias:
          type: string
          x-go-name: Alias
        expr:
          type: string
          x-go-name: Expr
      x-go-type:
        hints:
          noValidation: true
        import:
          alias: dbdatasets
          package: github.com/axiomhq/axiom/pkg/db/client/swagger/datasets
        type: VirtualColumn


````
