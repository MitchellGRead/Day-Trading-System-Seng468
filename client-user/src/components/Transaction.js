import React from 'react';

import TransactionTransact from './TransactionTransact';
import TransactionCommit from './TransactionCommit';
import TransactionCancel from './TransactionCancel';

const Transaction = (props) => {

  return (
    <div className='transaction'>
      <h3>Transactions</h3>
      <TransactionTransact userId={props.userId} onError={props.onError} />
      <TransactionCommit userId={props.userId} onError={props.onError} />
      <TransactionCancel userId={props.userId} onError={props.onError} />
    </div>
  )
}

export default Transaction