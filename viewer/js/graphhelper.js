var GraphHelper = (function () {

    /**
     * A graph helper.
     * @constructor
     */
    function GraphHelper(data, navigationAction, initialAction, intervalTime) {
        this.graphs = data;
        this.navigationAction = navigationAction;
        this.initialAction = initialAction;
        this.intervalTime = intervalTime;
        this.intervalToken = undefined;
        this.path = undefined;
        this.currentIndex = 0;
        this.started = false;
    }

    // Private callback function for setInterval.
    var onMove = function(self) {
        self.currentIndex++;
        if (self.started !== true || self.currentIndex >= self.path.length) {
            self.stopJourney();
            return;
        }

        self.navigationAction(self.path[self.currentIndex]);
    }

    /**
     * Sets the interval time.
     */
    GraphHelper.prototype.setIntervalTime = function (intervalTime) {
        this.intervalTime = intervalTime;
    }

     /**
     * Gets a value indicating whether a journey is started.
     */
    GraphHelper.prototype.getIsStarted = function() {
        return this.started;
    }

    /**
     * Calculate the shortest path between two nodes in a graph.
     * @param {Number} from
     * @param {Number} to
     * @return {Array} An array of node names corresponding to the path
     */
    GraphHelper.prototype.shortestPath = function (from, to) {
        var journeyGraph = undefined;
        for (var k in this.graphs) {
            if (this.graphs.hasOwnProperty(k)) {
                // Ensure that both nodes exist in the graph.
                if (this.graphs[k].nodes.indexOf(from) > -1 &&
                    this.graphs[k].nodes.indexOf(to) > -1) {
                    journeyGraph = this.graphs[k];
                    break;
                }
            }
        }

        if (journeyGraph === undefined) {
            return undefined;
        }

        var path = journeyGraph.nodes.sort();

        return path;
    }

    /**
     * Starts a journey between two nodes in a graph.
     * @param {Number} from
     * @param {Number} to
     */
    GraphHelper.prototype.startJourney = function (from, to) {
        if (this.started === true) {
            return;
        }

        this.path = this.shortestPath(from, to);
        if (this.path === undefined) {
            return;
        }

        this.started = true;
        this.currentIndex = 0;
        this.initialAction('walk');
        this.navigationAction(this.path[this.currentIndex])

        var _this = this;
        this.intervalToken = window.setInterval(function () { onMove(_this); }, this.intervalTime);
    }

    /**
     * Stops an ongoing journey between two nodes in a graph.
     */
    GraphHelper.prototype.stopJourney = function () {
        if (this.intervalToken === undefined) {
            return;
        }

        window.clearInterval(this.intervalToken);
        this.intervalToken = undefined;
        this.currentIndex = 0;
        this.path = undefined;

        this.started = false;
    }

    return GraphHelper;
})();