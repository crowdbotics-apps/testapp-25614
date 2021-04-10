import { createAppContainer } from 'react-navigation';
import { createStackNavigator } from 'react-navigation-stack';
import {createDrawerNavigator} from 'react-navigation-drawer';

import SplashScreen from "../features/SplashScreen";
import SideMenu from './sideMenu';
//@BlueprintImportInsertion
import BlankScreen14183522Navigator from '../features/BlankScreen14183522/navigator';
import BlankScreen13183278Navigator from '../features/BlankScreen13183278/navigator';
import BlankScreen12183277Navigator from '../features/BlankScreen12183277/navigator';
import BlankScreen11183276Navigator from '../features/BlankScreen11183276/navigator';
import BlankScreen10183275Navigator from '../features/BlankScreen10183275/navigator';
import BlankScreen9183274Navigator from '../features/BlankScreen9183274/navigator';
import BlankScreen8183273Navigator from '../features/BlankScreen8183273/navigator';
import BlankScreen7183272Navigator from '../features/BlankScreen7183272/navigator';
import BlankScreen6183271Navigator from '../features/BlankScreen6183271/navigator';
import BlankScreen5183270Navigator from '../features/BlankScreen5183270/navigator';
import BlankScreen4183269Navigator from '../features/BlankScreen4183269/navigator';
import BlankScreen3183268Navigator from '../features/BlankScreen3183268/navigator';
import BlankScreen1183266Navigator from '../features/BlankScreen1183266/navigator';
import BlankScreen0183265Navigator from '../features/BlankScreen0183265/navigator';

/**
 * new navigators can be imported here
 */

const AppNavigator = {

    //@BlueprintNavigationInsertion
BlankScreen14183522: { screen: BlankScreen14183522Navigator },
BlankScreen13183278: { screen: BlankScreen13183278Navigator },
BlankScreen12183277: { screen: BlankScreen12183277Navigator },
BlankScreen11183276: { screen: BlankScreen11183276Navigator },
BlankScreen10183275: { screen: BlankScreen10183275Navigator },
BlankScreen9183274: { screen: BlankScreen9183274Navigator },
BlankScreen8183273: { screen: BlankScreen8183273Navigator },
BlankScreen7183272: { screen: BlankScreen7183272Navigator },
BlankScreen6183271: { screen: BlankScreen6183271Navigator },
BlankScreen5183270: { screen: BlankScreen5183270Navigator },
BlankScreen4183269: { screen: BlankScreen4183269Navigator },
BlankScreen3183268: { screen: BlankScreen3183268Navigator },
BlankScreen1183266: { screen: BlankScreen1183266Navigator },
BlankScreen0183265: { screen: BlankScreen0183265Navigator },

    /** new navigators can be added here */
    SplashScreen: {
      screen: SplashScreen
    }
};

const DrawerAppNavigator = createDrawerNavigator(
  {
    ...AppNavigator,
  },
  {
    contentComponent: SideMenu
  },
);

const AppContainer = createAppContainer(DrawerAppNavigator);

export default AppContainer;
