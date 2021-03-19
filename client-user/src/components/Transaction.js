import React from 'react';

import TransactionTransact from './TransactionTransact';
import TransactionCommit from './TransactionCommit';
import TransactionCancel from './TransactionCancel';

const Transaction = (props) => {
  const userId = props.userId;
  const onError = props.onError;

  return (
    <div className='transaction'>
      <h3>Transactions</h3>
      <TransactionTransact userId={userId} onError={onError} />
      <TransactionCommit userId={userId} onError={onError} />
      <TransactionCancel userId={userId} onError={onError} />
    </div>
  )
}

export default Transaction