import React, { useState } from 'react';
import Quote from './components/Quote';
import UserCredentials from './components/UserCredentials';
import Transaction from './components/Transaction';
import Trigger from './components/Trigger';
import Add from './components/Add';
import Error from './components/Error';
import DisplaySummary from './components/DisplaySummary'
import Dumplog from './components/Dumplog'
import './styles/App.css';
import Success from './components/Success';

const App = () => {
  const [userId, setUserId] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');


  return (
    <div className="App">
      <div className='heading'>
        <h1>Stockadora Day Trading</h1>
        <UserCredentials
          userId={userId}
          onChangeUserId={setUserId}
          isAdmin={isAdmin}
          onChangeIsAdmin={setIsAdmin}
        />
      </div>
      { success !== '' &&
        <Success success={success} />
      }
      { error !== '' &&
        <Error error={error} />
      }
      <Quote userId={userId} onSuccess={setSuccess} onError={setError} />

      <div className='main-content'>
        <div className='account-actions'>
          <Add userId={userId} onSuccess={setSuccess} onError={setError} />
          <Transaction userId={userId} onSuccess={setSuccess} onError={setError} />
          <Trigger userId={userId} onSuccess={setSuccess} onError={setError} />
          <Dumplog userId={userId} onSuccess={setSuccess} isAdmin={isAdmin} onError={setError} />
        </div>
        <div className='summary-actions'>
          <DisplaySummary userId={userId} onSuccess={setSuccess} onError={setError} />
        </div>
      </div>

    </div>
  );
}

export default App;
