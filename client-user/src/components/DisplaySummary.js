import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { getDisplaySummary } from '../api';

const DisplaySummary = (props) => {
  const [loading, setLoading] = useState(false);
  const [userFunds, setUserFunds] = useState(0);
  const [stockHoldings, setStockHoldings] = useState([]);
  const [activeBuyTriggers, setActiveBuyTriggers] = useState([]);
  const [activeSellTriggers, setActiveSellTriggers] = useState([]);
  const { _, handleSubmit } = useForm();
  const userId = props.userId;
  const onError = props.onError;
  const onSuccess = props.onSuccess;

  const onSubmit = async () => {
    onSuccess('');
    onError('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let summaryData = await getDisplaySummary(userId);
      console.log(summaryData);
      setUserFunds(summaryData.funds);
      setActiveBuyTriggers(summaryData.active_buy_triggers);
      setActiveSellTriggers(summaryData.active_sell_triggers);
      setStockHoldings(summaryData.stock_holdings);
    } catch (error) {
      if (error.response.status === 404) {
        console.error(`Failed getting summary for ${userId}, make sure user exists (add funds).`)
      } else {
        console.error(error);
        onError(`${error.message} - Failed to fetch account summary`)
      }
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