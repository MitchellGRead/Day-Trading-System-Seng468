// Initialization script for the mongoDb database

db = db.getSiblingDB("trading-db");
db.logs.insertOne(
	{user_id: "", logs: []}
);
