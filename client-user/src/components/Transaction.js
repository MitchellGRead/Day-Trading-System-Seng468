import React from 'react';

import TransactionTransact from './TransactionTransact';
import TransactionCommit from './TransactionCommit';
import TransactionCancel from './TransactionCancel';

const Transaction = (props) => {
  const userId = props.userId;
  const onError = props.onError;
  const onSuccess = props.onSuccess;

  return (
    <div className='transaction'>
      <h3>Transactions</h3>
      <TransactionTransact userId={userId} onSuccess={onSuccess} onError={onError} />
      <TransactionCommit userId={userId} onSuccess={onSuccess} onError={onError} />
      <TransactionCancel userId={userId} onSuccess={onSuccess} onError={onError} />
    </div>
  )
}

export default Transaction