INSERT INTO dbo.SalesData
(SalesOrderID, SalesOrderDetailID, OrderQuantity, ProductID, UnitPrice, UnitPriceDiscount,
ModifiedDate, OrderDate, ShipDate, Status, SalesOrderNumber, CustomerID, SalesPersonID,
PersonID, BusinessEntityID, Title, FirstName, MiddleName, LastName, EmailAddress,
AddressID, AddressLine)

SELECT 
Sales.SalesOrderDetail.SalesOrderID,
Sales.SalesOrderDetail.SalesOrderDetailID,
Sales.SalesOrderDetail.OrderQty,
Sales.SalesOrderDetail.ProductID,
Sales.SalesOrderDetail.UnitPrice,
Sales.SalesOrderDetail.UnitPriceDiscount,
Sales.SalesOrderDetail.ModifiedDate,

Sales.SalesOrderHeader.OrderDate,
Sales.SalesOrderHeader.ShipDate,
Sales.SalesOrderHeader.Status,
Sales.SalesOrderHeader.SalesOrderNumber,
Sales.SalesOrderHeader.CustomerID,
Sales.SalesOrderHeader.SalesPersonID,

Sales.Customer.PersonID,

Person.BusinessEntityContact.BusinessEntityID,

Person.Person.Title,
Person.Person.FirstName,
Person.Person.MiddleName,
Person.Person.LastName,

Person.EmailAddress.EmailAddress,

Person.BusinessEntityAddress.AddressID,

Person.Address.AddressLine1

FROM

Sales.SalesOrderDetail
INNER JOIN
Sales.SalesOrderHeader
ON
Sales.SalesOrderDetail.SalesOrderID = Sales.SalesOrderHeader.SalesOrderID

INNER JOIN
Sales.Customer
ON
Sales.SalesOrderHeader.CustomerID = Sales.Customer.CustomerID

INNER JOIN
Person.BusinessEntityContact
ON
Sales.Customer.PersonID = Person.BusinessEntityContact.PersonID

INNER JOIN
Person.Person
ON
Person.Person.BusinessEntityID = Person.BusinessEntityContact.BusinessEntityID

INNER JOIN
Person.EmailAddress
ON
Person.Person.BusinessEntityID = Person.EmailAddress.BusinessEntityID

INNER JOIN
Person.BusinessEntityAddress
ON
Person.BusinessEntityContact.BusinessEntityID = Person.BusinessEntityAddress.BusinessEntityID

INNER JOIN
Person.Address
ON
Person.BusinessEntityAddress.AddressID = Person.Address.AddressID

ORDER BY NEWID()
