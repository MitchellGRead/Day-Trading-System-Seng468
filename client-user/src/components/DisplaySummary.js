import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { getDisplaySummary } from '../api';
import ActiveTrigger from './ActiveTrigger';
import StockHolding from './StockHolding';

const DisplaySummary = (props) => {
  const [loading, setLoading] = useState(false);
  const [userFunds, setUserFunds] = useState(0);
  const [reserveFunds, setReserveFunds] = useState(0);
  const [stockHoldings, setStockHoldings] = useState([]);
  const [activeTriggers, setActiveTriggers] = useState([]);
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
      let resp = await getDisplaySummary(userId);
      let summaryData = resp.data;

      setUserFunds(summaryData.user_funds.available_funds);
      setReserveFunds(summaryData.user_funds.reserved_funds);
      setStockHoldings(formatHoldings(summaryData.stock_holdings));


      let buyTriggers = formatTriggers(summaryData.active_buy_triggers, 'Buy');
      let sellTriggers = formatTriggers(summaryData.active_sell_triggers, 'Sell');
      setActiveTriggers(buyTriggers.concat(sellTriggers));
    } catch (error) {
      console.log(error);
      let status = error.response.status;
      if (status === 404) {
        onError(`Failed getting summary for ${userId}, make sure user exists (add funds).`)
      } else if (status === 400) {
        onError(error.response.data.errorMessage);
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
      return {
        'stockSymbol': symbol,
        'shares': holding,
        'reserved': reserved === 0 ? 0 : reserved
      };
    });

    return formattedHoldings;
  };

  const formatTriggers = (triggers, triggerType) => {
    let formattedTriggers = Object.keys(triggers).map(symbol => {
      let [shares, executionPrice,] = triggers[symbol];
      return {
        'triggerType': triggerType,
        'shares': shares,
        'stockSymbol': symbol,
        'executionPrice': executionPrice
      };
    });

    return formattedTriggers;
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
          {
            activeTriggers.map(trigger => {
              return <ActiveTrigger
                key={trigger.stockSymbol + '-' + trigger.triggerType}
                triggerType={trigger.triggerType}
                stockSymbol={trigger.stockSymbol}
                shares={trigger.shares}
                executionPrice={trigger.executionPrice}
              />
            })
          }
        </div>
        <div className='stock-holdings'>
          <h4>Stock Holdings:</h4>
          {
            stockHoldings.map(holding => {
              return <StockHolding
                key={holding.stockSymbol}
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