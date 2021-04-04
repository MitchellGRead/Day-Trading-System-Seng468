import React from 'react';

const ActiveTrigger = (props) => {
  const triggerType = props.triggerType;
  const stockSymbol = props.stockSymbol;
  const shares = props.shares;
  const executionPrice = props.executionPrice;

  return (
    <div className='active-trigger'>
      <span>Type: {triggerType}</span>
      <span>Symbol: {stockSymbol}</span>
      <span>Shares to {triggerType}: {shares.toLocaleString()}</span>
      <span>Execute price: ${executionPrice.toLocaleString()}</span>
    </div>
  )
};

export default ActiveTrigger;