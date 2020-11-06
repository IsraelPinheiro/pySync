# PySync

## Equipe

- Israel Pinheiro
- Ricassio Costa
- Lucas Gomes

## Message Transfer Protocol

### Register User

- Client Request

```jsonc
{
    "Action":"RegisterUser",
    "Timestamp":1604061231.0383,
    "User":{
        "Email":"usuario01@pysync.com",
        "Password":"minhasenhasuperdificil"
    }
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200 //OK - User Registered
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Outside the expected format for the type of action
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - E-mail already registered
}
```

### Register Agent

- Client Request

```jsonc
{
    "Action":"RegisterAgent",
    "Timestamp":1604061231.0383,
    "Agent":{
        "Name":"PC Casa",
        "User":{
            "Email":"usuario01@pysync.com",
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Password MD5 Hash
        }
    }
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200 //OK - Agent Registered
}

{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Outside the expected format for the type of action
}
```

### New File

- Client Request

```jsonc
{
    "Action":"Create",
    "Timestamp":1604061231.0383,
    "Agent":{
        "Key":"6C19A781148814833ED25840B7A07BA7",
        "User":{
            "Email":"usuario01@pysync.com",
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Password MD5 Hash
        }
    },
    "File":{
        "OriginalName":"Arquivo01.txt",
        "Size":"32253" //Size, in bytes, of the file
    }
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200 //OK - File Created
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":100 //Continue - Server ready to receive the file
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Outside the expected format for the type of action
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - Unauthorized User or Agent
}
```

### Update File

- Client Request

```jsonc
{
    "Action":"Update",
    "Timestamp":1604061231.0383,
    "Agent":{
        "Key":"6C19A781148814833ED25840B7A07BA7",
        "User":{
            "Email":"usuario01@pysync.com",
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Password MD5 Hash
        }
    },
    "File":{
        "Name":"BBE02F946D5455D74616FC9777557C22",
        "Size":"32253" //Size, in bytes, of the file
    }
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200 //OK - File Updated
}
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":100 //Continue - Server ready to receive the file
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Outside the expected format for the type of action
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - Unauthorized User or Agent
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":404 //Not Found - Arquivo não localizado
}
```

### Delete File

- Client Request

```jsonc
{
    "Action":"Delete",
    "Timestamp":1604061231.0383,
    "Agent":{
        "Key":"6C19A781148814833ED25840B7A07BA7",
        "User":{
            "Email":"usuario01@pysync.com",
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Password MD5 Hash
        }
    },
    "File":"BBE02F946D5455D74616FC9777557C22"  
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200 //OK - File Deleted
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":100 //Continue - Server ready to receive the file
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Outside the expected format for the type of action
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - Unauthorized User or Agent
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":404 //Not Found - Arquivo não localizado
}
```

### Get Remote Changes

- Client Request

```jsonc
{
    "Action":"GetChanges",
    "Timestamp":1604061231.0383,
    "Agent":{
        "Key":"6C19A781148814833ED25840B7A07BA7",
        "User":{
            "Email":"usuario01@pysync.com",
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Password MD5 Hash
        }
    }
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200, //OK
    "Changes":{
        "Created":[
            {
                "OriginalName":"Arquivo01.txt",
                "Size":"32253" //Size, in bytes, of the file
            },
            {
                "OriginalName":"Arquivo02.txt",
                "Size":"32253" //Size, in bytes, of the file
            }
        ],
        "Updated":[
            {
                "OriginalName":"Arquivo03.txt",
                "Size":"32253" //Size, in bytes, of the file
            },
            {
                "OriginalName":"Arquivo04.txt",
                "Size":"32253" //Size, in bytes, of the file
            }
        ],
        "Deleted":[
            {
                "OriginalName":"Arquivo05.txt",
                "Size":"32253" //Size, in bytes, of the file
            },
            {
                "OriginalName":"Arquivo06.txt",
                "Size":"32253" //Size, in bytes, of the file
            }
        ]
    }
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Outside the expected format for the type of action
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - Unauthorized User or Agent
}
```
