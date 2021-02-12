// Initiliaztion script for the mongoDb database

db = db.getSiblingDB("trading-db");
db.logs.insertOne(
	{user_id: "", logs: [""]}
);
db.triggers.insertOne(
	{
		user_id: "", 
		buy_amounts: [{trigger_id: "", stock_id: "", buy_amount: ""}],
		buy_triggers: [{trigger_id: "", stock_id: "", buy_price: ""}],
		sell_amounts: [{trigger_id: "", stock_id: "", sell_amount: ""}],
		sell_triggers: [{trigger_id: "", stock_id: "", sell_price: ""}]
	}
);