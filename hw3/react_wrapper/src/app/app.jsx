(function () {
    let React = require('react');
    let ReactDOM = require('react-dom');
    let injectTapEventPlugin = require('react-tap-event-plugin');
    let Main = require('./components/main.jsx'); // Our custom react component
    let ReactRouterHistory = (require('history/lib/createBrowserHistory'))();

    var Master = require("./master.jsx");
    var D3Gallery = require('./components/d3/d3gallery.jsx');
    var Banana = require('./components/banana/banana.jsx');
    var FacetView = require('./components/facet/facetView.jsx');
    var MapView = require('./components/map/mapView.jsx');
    const {
        Router,
        Route,
        Redirect,
        IndexRoute,
        } = require('react-router');
    //Needed for React Developer Tools
    window.React = React;

    //Needed for onTouchTap
    //Can go away when react 1.0 release
    //Check this repo:
    //https://github.com/zilverline/react-tap-event-plugin
    injectTapEventPlugin();


    // define routes
    var routes =
        <Router
            history={ReactRouterHistory}
            onUpdate={() => window.scrollTo(0, 0)}>
            <Route component={Master} path="/">
                <Route component={D3Gallery} path="/d3"/>
                <Route component={Banana} path="/banana"/>
                <Route component={FacetView} path="/facet"/>
                <Route component={MapView} path="/map"/>
            </Route>
        </Router>;

    // Render the main app react component into the app div.
    // For more details see: https://facebook.github.io/react/docs/top-level-api.html#react.render
    ReactDOM.render(routes
        , document.getElementById('app'));

})();
