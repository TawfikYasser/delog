SELECT * FROM sd_db.salesdata;

UPDATE sd_db.salesdata SET sd_db.salesdata.SalesOrderNumber = sd_db.salesdata.CustomerID / sd_db.salesdata.PersonID
WHERE sd_db.salesdata.MiddleName is null;

DELETE FROM sd_db.salesdata;

UPDATE sd_db.salesdata SET sd_db.salesdata.Gender = 'Male' WHERE sd_db.salesdata.Title = 'Mr.';
UPDATE sd_db.salesdata SET sd_db.salesdata.Gender = 'Female' WHERE sd_db.salesdata.Title = 'Ms.';



UPDATE sd_db.salesdata SET sd_db.salesdata.Title = 'Ms.'
WHERE sd_db.salesdata.Title = 'Mr.' AND sd_db.salesdata.UnitPrice > 300.00 AND sd_db.salesdata.ProductID %2 = 0;


UPDATE sd_db.salesdata 
SET sd_db.salesdata.EmailAddress = concat(salesdata.Gender ,'@', substring(sd_db.salesdata.AddressLine,1,4), sd_db.salesdata.LastName,'.net')
WHERE sd_db.salesdata.PersonID > 465;
