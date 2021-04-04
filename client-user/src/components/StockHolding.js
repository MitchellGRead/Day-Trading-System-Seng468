import React from 'react';

const StockHolding = (props) => {
  const stockSymbol = props.stockSymbol;
  const stockHeld = props.stockHeld;
  const stockReserved = props.stockReserved;

  return (
    <div className='stock-holding'>
      <span>Symbol: {stockSymbol}</span>
      <span>Current Shares: {stockHeld}</span>
      <span>Shares Reserved: {stockReserved}</span>
    </div>
  );
};

export default StockHolding;