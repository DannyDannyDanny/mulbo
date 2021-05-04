# Mulbo
Mulbo - APIs, front-ends, back-ends and maybe audio experiments

```
                               88 88                       
                               88 88                       
                               88 88                       
88,dPYba,,adPYba,  88       88 88 88,dPPYba,   ,adPPYba,   
88P'   "88"    "8a 88       88 88 88P'    "8a a8"     "8a  
88      88      88 88       88 88 88       d8 8b       d8  
88      88      88 "8a,   ,a88 88 88b,   ,a8" "8a,   ,a8"  
88      88      88  `"YbbdP'Y8 88 8Y"Ybbd8"'   `"YbbdP"'   

| Media Directory |     | Mulbo (Python) |     | Index (sqlite)|
| ( put media     | <-> | (checks new    | <-> | (new files    |
| files in here ) |     |  media files ) |     |  added to db) |

1) check for media not already in index
2) add any new files to index (filename, path, filesize)

Tables
| files |       | audio   |
|:-----:|       |:-------:|
| id    | <-|   | id      |
| name  |   |-> | file_id |
| path  |       | ????    |
```

## Contributing
You've stubmled over a hobby project.

* [ASCII mulbo](https://ascii.co.uk/art/MULBO)
