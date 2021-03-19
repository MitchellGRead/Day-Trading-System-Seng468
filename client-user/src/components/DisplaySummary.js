import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { getDisplaySummary } from '../api';

const DisplaySummary = (props) => {
  const [loading, setLoading] = useState(false);
  const [userFunds, setUserFunds] = useState(0);
  const [transactionHistory, setTransactionHistory] = useState([]);
  const [activeTriggers, setactiveTriggers] = useState([]);
  const { _, handleSubmit } = useForm();
  const userId = props.userId;
  const onError = props.onError;

  const onSubmit = async () => {
    onError('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let summaryData = await getDisplaySummary(userId);
      // TODO set the states for the summary
      // TODO set and handle error
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to fetch account summary`)
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className='display-summary'>
      <h3>Account Summary</h3>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input
          type='submit'
          disabled={loading}
          value={loading ? 'Fetching...' : 'Get Account Summary'}
        />
      </form>
      <span className='userFunds'>Current funds: {userFunds}</span>
      <div className='triggers-and-history'>
        <div className='active-triggers'>
          <h4>Active Triggers:</h4>
          {/* TODO make active triggers objects once audit service finished */}
        </div>
        <div className='transaction-history'>
          <h4>Transaction History:</h4>
          {/* TODO make transaction history objects once audit service finished  */}
        </div>
      </div>
    </div>

  );
};

export default DisplaySummary;