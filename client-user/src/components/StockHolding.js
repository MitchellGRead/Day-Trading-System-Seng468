import React from 'react';

const StockHolding = (props) => {
  const stockSymbol = props.stockSymbol;
  const stockHeld = props.stockHeld;
  const stockReserved = props.stockReserved;

  return (
    <div className='stock-holding'>
      <span>Symbol: {stockSymbol}</span>
      <span>Current Shares: {stockHeld.toLocaleString()}</span>
      <span>Shares Reserved: {stockReserved.toLocaleString()}</span>
    </div>
  );
};

export default StockHolding;