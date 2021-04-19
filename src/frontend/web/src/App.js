import AppRouter from './router/app_router'
import background from './background_2.jpg'

function App() {
   const container = {
        backgroundImage: `url(${background})`,
        backgroundPosition: 0,
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        width: '100vw',
        height: '100vh'
    };
  
  function onMove(e) {
    console.log(e.nativeEvent.screenX)
  }

  return (
    <div className="App" style={container} /*onMouseMove={onMove}>*/ > 
      {/* <img src={background}/> */}
        <AppRouter/>
    </div>
  );
}

export default App;
