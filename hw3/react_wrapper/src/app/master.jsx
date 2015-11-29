const React = require('react');
const Router = require('react-router');
const AppLeftNav = require('./app-left-nav.jsx');
const { AppBar,
    AppCanvas,
    FontIcon,
    IconButton,
    EnhancedButton,
    Menu,
    Mixins,
    RaisedButton,
    Styles,
    Tab,
    Tabs,
    Paper} = require('material-ui');
import {Link} from 'react-router'

const { StylePropable } = Mixins;
const { Colors, Spacing, Typography } = Styles;
const ThemeManager = Styles.ThemeManager;
const DefaultRawTheme = Styles.LightRawTheme;


const Master = React.createClass({
    mixins: [StylePropable],

    getInitialState () {
        let muiTheme = ThemeManager.getMuiTheme(DefaultRawTheme);
        // To switch to RTL...
        // muiTheme.isRtl = true;
        return {
            muiTheme,
        };
    },

    childContextTypes: {
        muiTheme: React.PropTypes.object,
    },

    getChildContext() {
        return {
            muiTheme: this.state.muiTheme,
        };
    },

    getStyles() {
        let darkWhite = Colors.darkWhite;
        return {
            footer: {
                backgroundColor: Colors.grey900,
                textAlign: 'center',
            },
            a: {
                color: darkWhite,
            },
            p: {
                margin: '0 auto',
                padding: 0,
                color: Colors.lightWhite,
                maxWidth: 335,
            },
            github: {
                position: 'fixed',
                right: Spacing.desktopGutter / 2,
                top: 8,
                zIndex: 5,
                color: 'white',
            },
            iconButton: {
                color: darkWhite,
            },
            titlebar: {
                position: "fixed"
            },
            content: {
                padding: 8,
                width: "100%",
                position: "absolute",
                top: '64px',
            }
        };
    },

    componentWillMount() {
        let newMuiTheme = this.state.muiTheme;
        newMuiTheme.inkBar.backgroundColor = Colors.yellow200;
        this.setState({
            muiTheme: newMuiTheme,
            tabIndex: this._getSelectedIndex()
        });
        let setTabsState = function () {
            this.setState({renderTabs: !(document.body.clientWidth <= 647)});
        }.bind(this);
        setTabsState();
        window.onresize = setTabsState;
    },

    componentWillReceiveProps(nextProps, nextContext) {
        let newMuiTheme = nextContext.muiTheme ? nextContext.muiTheme : this.state.muiTheme;
        this.setState({
            tabIndex: this._getSelectedIndex(),
            muiTheme: newMuiTheme,
        });
    },

    render() {
        let styles = this.getStyles();
        let title =
            this.props.history.isActive('/get-started') ? 'Get Started' :
                this.props.history.isActive('/customization') ? 'Customization' :
                    this.props.history.isActive('/components') ? 'Components' : '';

        return (
            <AppCanvas>
                {this.state.renderTabs ? this._getTabs(): this._getAppBar()}

                <div style={styles.content}>
                    {this.props.children || <h1>WELCOME</h1>}
                </div>
                <AppLeftNav ref="leftNav" history={this.props.history}/>
            </AppCanvas>
        );
    },

    _getTabs() {
        let styles = {
            root: {
                backgroundColor: Colors.cyan500,
                position: 'fixed',
                height: 64,
                top: 0,
                right: 0,
                zIndex: 4,
                width: '100%',
            },
            container: {
                position: 'absolute',
                right: (Spacing.desktopGutter / 2) + 12,
                bottom: 0,
            },
            span: {
                color: Colors.white,
                fontWeight: Typography.fontWeightLight,
                left: 5,
                top: 22,
                position: 'absolute',
                fontSize: 26,
            },
            svgLogoContainer: {
                position: 'fixed',
                width: 300,
                left: Spacing.desktopGutter,
            },
            svgLogo: {
                width: 65,
                backgroundColor: Colors.cyan500,
                position: 'absolute',
                top: 20,
            },
            tabs: {
                width: 425,
                bottom: 0,
            },
            tab: {
                height: 64,
            },

        };

        let materialIcon = (
            <EnhancedButton
                style={styles.svgLogoContainer}>
                <Link to={this._getRoute()}>
                    <span style={this.prepareStyles(styles.span)}>{this._getTitle()}</span>
                </Link>
            </EnhancedButton>);

        return (
            <div>
                <Paper
                    zDepth={0}
                    rounded={false}
                    style={styles.root}>
                    {materialIcon}
                    <div style={this.prepareStyles(styles.container)}>
                        <Tabs
                            style={styles.tabs}
                            value={this.state.tabIndex}
                            onChange={this._handleTabChange}>
                            <Tab
                                value="1"
                                label="D3"
                                style={styles.tab}
                                route="/d3"/>
                            <Tab
                                value="2"
                                label="Banana"
                                style={styles.tab}
                                route="/banana"/>
                            <Tab
                                value="3"
                                label="Facet"
                                style={styles.tab}
                                route="/facet"/>
                            <Tab
                                value="4"
                                label="Map"
                                style={styles.tab}
                                route="/map"/>
                        </Tabs>
                    </div>
                </Paper>
            </div>
        );
    },

    _getSelectedIndex() {
        return this.props.history.isActive('/d3') ? '1' :
            this.props.history.isActive('/banana') ? '2' :
                this.props.history.isActive('/facet') ? '3' :
                    this.props.history.isActive('/map') ? '4' : '0';
    },

    _handleTabChange(value, e, tab) {
        this.props.history.pushState(null, tab.props.route);
        this.setState({tabIndex: this._getSelectedIndex()});
    },

    _getTitle() {
        "use strict";
        return this.props.history.isActive('/d3') ? 'D3 Gallery' :
            this.props.history.isActive('/banana') ? 'Banana' :
                this.props.history.isActive('/facet') ? 'Facet View' :
                    this.props.history.isActive('/map') ? 'Map' : 'Solr Weapon';

    },
    _getRoute() {
        "use strict";
        return this.props.history.isActive('/d3') ? '/d3' :
            this.props.history.isActive('/banana') ? '/banana' :
                this.props.history.isActive('/facet') ? '/facet' :
                    this.props.history.isActive('/map') ? '/map' : 'Solr Weapon';

    },
    _getAppBar() {
        let title =
            //this.props.history.isActive('/get-started') ? 'Get Started' :
            //    this.props.history.isActive('/customization') ? 'Customization' :
            //        this.props.history.isActive('/components') ? 'Components' : '';
            this.props.history.isActive('/d3') ? 'D3 Gallery' :
                this.props.history.isActive('/banana') ? 'Banana' :
                    this.props.history.isActive('/facet') ? 'Facet View' :
                        this.props.history.isActive('/map') ? 'Map' : 'Solr Weapon';

        return (
            <AppBar
                onLeftIconButtonTouchTap={this._onLeftIconButtonTouchTap}
                title={title}
                zDepth={0}
                style={{position: 'absolute', top: 0}}/>
        );
    },

    _onLeftIconButtonTouchTap() {
        this.refs.leftNav.toggle();
    },
});

module.exports = Master;
