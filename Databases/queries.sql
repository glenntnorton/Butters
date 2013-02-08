CREATE TABLE login ( 
    id INTEGER NOT NULL PRIMARY KEY , 
    username VARCHAR ( 64 ) NOT NULL , 
    passwd LONGBLOB NOT NULL , 
    created INTEGER NOT NULL 
) ; 
