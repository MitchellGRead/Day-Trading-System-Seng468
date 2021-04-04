import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { getDisplaySummary } from '../api';
import StockHolding from './StockHolding';

const DisplaySummary = (props) => {
  const [loading, setLoading] = useState(false);
  const [userFunds, setUserFunds] = useState(0);
  const [reserveFunds, setReserveFunds] = useState(0);
  const [stockHoldings, setStockHoldings] = useState([]);
  const [activeBuyTriggers, setActiveBuyTriggers] = useState({});
  const [activeSellTriggers, setActiveSellTriggers] = useState({});
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

      setUserFunds(summaryData.user_funds.available_funds);
      setReserveFunds(summaryData.user_funds.reserved_funds);
      formatHoldings(summaryData.stock_holdings);

      setActiveBuyTriggers(summaryData.active_buy_triggers);
      setActiveSellTriggers(summaryData.active_sell_triggers);
    } catch (error) {
      if (error.response.status === 404) {
        onError(`Failed getting summary for ${userId}, make sure user exists (add funds).`)
      } else {
        console.error(error);
        onError(`${error.message} - Failed to fetch account summary`)
      }
    } finally {
      setLoading(false);
    }
  };

  const formatHoldings = (holdings) => {
    let formattedHoldings = Object.keys(holdings).map(symbol => {
      let [holding, reserved] = holdings[symbol];
      console.log(symbol);
      return {
        'stockSymbol': symbol,
        'shares': holding,
        'reserved': reserved === 0 ? 0 : reserved
      };
    });

    setStockHoldings(formattedHoldings);
  };

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
      <span className='userFunds'>Current funds: ${userFunds.toLocaleString()}</span>
      <span className='userFunds'>Reserved funds: ${reserveFunds.toLocaleString()}</span>
      <div className='triggers-and-history'>
        <div className='active-triggers'>
          <h4>Active Triggers:</h4>
          {/* TODO make active triggers objects once audit service finished */}
        </div>
        <div className='stock-holdings'>
          <h4>Stock Holdings:</h4>
          {
            stockHoldings.map(holding => {
              return <StockHolding
                id={holding.stockSymbol}
                stockSymbol={holding.stockSymbol}
                stockHeld={holding.shares}
                stockReserved={holding.reserved}
              />
            })
          }
        </div>
      </div>
    </div>

  );
};

export default DisplaySummary;