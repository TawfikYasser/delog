SELECT * FROM sd_db.salesdata;
-- Data Manipulation
DELETE FROM sd_db.salesdata;
UPDATE sd_db.salesdata SET sd_db.salesdata.MiddleName = 'Unknown' WHERE sd_db.salesdata.MiddleName IS NULL;

-- Completeness
UPDATE sd_db.salesdata SET sd_db.salesdata.FirstName = '' WHERE sd_db.salesdata.MiddleName IS NULL AND sd_db.salesdata.Gender = 'Female';
-- Accuracy
UPDATE sd_db.salesdata SET sd_db.salesdata.SalesOrderNumber = FLOOR(sd_db.salesdata.CustomerID / sd_db.salesdata.PersonID)
WHERE sd_db.salesdata.MiddleName is null;
-- Consistency
UPDATE sd_db.salesdata SET sd_db.salesdata.Title = 'Ms.'
WHERE sd_db.salesdata.Title = 'Mr.' AND sd_db.salesdata.UnitPrice < 300.00 AND sd_db.salesdata.ProductID %2 = 0;
-- Validity
UPDATE sd_db.salesdata 
SET sd_db.salesdata.EmailAddress =
 concat(substring(sd_db.salesdata.Address,1,4), sd_db.salesdata.LastName,'.net')
WHERE sd_db.salesdata.PersonID < 465;

