# PySync

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
    "Status":200 //OK - User registered
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Fora do padrão esperado para o tipo de ação
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - Email Já cadastrado
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
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Hash MD5 da Senha
        }
    }
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200 //OK - User registered
}

{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Fora do padrão esperado para o tipo de ação
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
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Hash MD5 da Senha
        }
    },
    "File":{
        "OriginalName":"Arquivo01.txt",
        "Size":"32253" //Tamanho, em bytes, do arquivo
    }
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200 //OK - User registered
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":100 //Continue - Servidor aguardando envio do arquivo
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Fora do padrão esperado para o tipo de ação
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - User ou Agent não autorizado
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
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Hash MD5 da Senha
        }
    },
    "File":{
        "Name":"BBE02F946D5455D74616FC9777557C22",
        "Size":"32253" //Tamanho, em bytes, do arquivo
    }
}
```

- Possible Server Responses

```jsonc
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":200 //OK - User registered
}
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":100 //Continue - Servidor aguardando envio do arquivo
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Fora do padrão esperado para o tipo de ação
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - User ou Agent não autorizado
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
            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0" //Hash MD5 da Senha
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
    "Status":200 //OK - User registered
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":100 //Continue - Servidor aguardando envio do arquivo
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":400 //Bad Request - Fora do padrão esperado para o tipo de ação
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":403 //Denied - User ou Agent não autorizado
},
{
    "Action":"ServerResponse",
    "Timestamp":1604061231.0383,
    "Status":404 //Not Found - Arquivo não localizado
}
```
