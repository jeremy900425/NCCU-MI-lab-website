## Please folowing tutorial
https://aws.amazon.com/tw/getting-started/hands-on/create-connect-postgresql-db/

## Notice
### Make sure the following settings or status
- Status : Available
- Multi-AZ : NO
- Port : 5432
- Security groups : Add in bound rule
  - {Type:PostgreSQL, Protocal:TCP, Port range:5432, Source:Anywhere}
- Publicly accessible : Yes
- DB name != DB identifier
  - If your DB name is '-', Default is postgres
  - Make sure your URL is correct,like 
  - `jdbc:postgresql://mydb.......amazonaws.com:5432/postgres`