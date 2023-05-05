SELECT * FROM Flights WHERE from_airport_id = 2;

SELECT * FROM Flights WHERE from_airport_id = 3;



WITH FromAirp AS (SELECT * FROM Flights WHERE from_airport_id = 2),
ToAirp AS (SELECT * FROM Flights WHERE to_airport_id = 5),
Mid AS (SELECT * FROM Flights)
SELECT * FROM FromAirp, Mid, ToAirp WHERE FromAirp.to_airport_id = Mid.from_airport_id AND Mid.to_airport_id = ToAirp.from_airport_id