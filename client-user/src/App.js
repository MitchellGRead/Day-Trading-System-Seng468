import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import Quote from './components/Quote';
import UserCredentials from './components/UserCredentials';
import Transaction from './components/Transaction';
import Add from './components/Add';
import Error from './components/Error';
import './styles/App.css';

const App = (props) => {
  const [userId, setUserId] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [error, setError] = useState('');

  console.log(userId, isAdmin)

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
      <Error error={error} />
      <Quote userId={userId} onError={setError} />

      <div className='main-content'>
        <Add userId={userId} onError={setError} />
        <Transaction userId={userId} onError={setError} />
      </div>

    </div>
  );
}

export default App;
