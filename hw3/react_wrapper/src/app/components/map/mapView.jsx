import React from 'react'
var ReactScriptLoaderMixin = require('react-script-loader').ReactScriptLoaderMixin;

var Khooshe = React.createClass({

    autoResize() {
        var newHeight;
        var newWidth;
        "use strict";
        if (this.refs.iframe1) {
            newHeight = this.refs.iframe1.contentWindow.document.body.scrollHeight;
            newWidth = this.refs.iframe1.contentWindow.document.body.scrollWidth;
        }

        this.refs.iframe1.style.height = (newHeight) + "px";
        //this.refs.iframe1.style.width = (newWidth) + "px";
    },
    render() {
        "use strict";
        var _style = {
            width: "100%",
        };
        return (
            <div style={_style}>
                <iframe src="/visualizer/khoose_visualizer.html" width="100%" scrolling="no"
                        ref="iframe1"
                        frameBorder="0" onLoad={this.autoResize}></iframe>

            </div>
        );
    }

});
export default Khooshe;