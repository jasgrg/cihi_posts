import React, { useState } from 'react';
//import logo from './logo.svg';
import logo from './assets/cihi.png';
import './App.css';
import FacebookLogin, { ReactFacebookFailureResponse, ReactFacebookLoginInfo } from 'react-facebook-login';
import moment from 'moment';

interface FacebookLoginResult extends ReactFacebookLoginInfo, ReactFacebookFailureResponse{
  data_access_expiration_time: number;
}

interface SetTokenResponse {
  valid: boolean;
}

function post_token(token: ReactFacebookLoginInfo): Promise<Response> {
  return fetch("https://ncfjzkpa66.execute-api.us-east-1.amazonaws.com/v1",
    {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": 'application/json'
      },
      body: JSON.stringify(token)
    }
  );
}

function getSuccessMessage(data: FacebookLoginResult) {
  return `Success! Your token is good until ${moment.unix(data.data_access_expiration_time).format("LL")}`;
}

function App() {

  const [login, setLogin] = useState(false);
  const [data, setData] = useState<FacebookLoginResult>();
  
  const responseFacebook = (response: any) => {
    console.log(response);
    if (response.accessToken) {
      setLogin(true);
      post_token(response).then((setTokenResponse: Response) => {
        setTokenResponse.json().then((value: SetTokenResponse) => {
          if(value && value.valid) {
            setData(response);
          }
        });
      });
    } else {
      setLogin(false);
    }
  }

  return (
    <>
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          { !login && 
          <FacebookLogin
          appId="1575161736262942"
          autoLoad={true}
          fields="name,email"
          scope="user_managed_groups,groups_show_list,groups_access_member_info"
          callback={responseFacebook}
          icon="fa-facebook" />
          }
          { login && data && getSuccessMessage(data) }
        </p>
      </header>
    </div>
    </>
  );
}

export default App;
