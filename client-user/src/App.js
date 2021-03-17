import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import UserCredentials from './components/UserCredentials';
import './styles/App.css';

const App = (props) => {
  const [userId, setUserId] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);

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

    </div>
  );
}

export default App;
