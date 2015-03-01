var Dijkstra = (function () {

     /**
     * A class for calculations on graphs using Dijkstra's algorithm.
     * @constructor
     */
    function Dijkstra() {
    }

    // Private sort delegate for ordering key value pairs arranged
    // as an array of two items like [key, value].
    var keyValueSorter = function (kv1, kv2) {
        return parseFloat(kv1[1]) - parseFloat(kv2[1]);
    }

     /**
     * Calculate the shortest path between two nodes in a graph using
     * Dijkstra's Algorithm.
     * @param {Object} graph
     * @param {String} source
     * @param {String} target
     * @return {Array} An array of node names corresponding to the path
     */
    Dijkstra.prototype.shortestPath = function (graph, source, target, weight) {
        if (source === target) {
            return [source];
        }

        var touchedNodes = {};
        var previous = {};
        var distances = {};
        var visited = {};

        touchedNodes[source] = 0;
        previous[source] = undefined;
        distances[source] = 0;

        while (true) {
            var touched = [];
            for (var key in touchedNodes) {
                if (Object.prototype.hasOwnProperty.call(touchedNodes, key)) {
                    touched.push([key, touchedNodes[key]])
                }
            }

            // Stop if none of the unvisited nodes can be reached.
            if (!touched.length) {
                break;
            }

            // Select the unvisited node with smallest distance and mark it as current node.
            touched.sort(keyValueSorter);
            var currentNode = touched[0][0];

            visited[currentNode] = true;
            delete touchedNodes[currentNode];

            // Return if we have reached the target.
            if (currentNode === target) {
                break;
            }

            var currentEdges = graph.edges[currentNode] || {};

            for (var node in currentEdges) {
                if (Object.prototype.hasOwnProperty.call(currentEdges, node)) {

                    // Do not process already visited nodes.
                    if (Object.prototype.hasOwnProperty.call(visited, node)) {
                        continue;
                    }

                    // Calculate the total distance from the source to the node of
                    // the current edge.
                    var distance = currentEdges[node][weight];
                    var totalDistance = distances[currentNode] + distance;

                    if (!distances[node] || totalDistance < distances[node])
                    {
                        distances[node] = totalDistance;
                        touchedNodes[node] = totalDistance;
                        previous[node] = currentNode;
                    }
                }
            }
        }

        // No path to the target was found.
        if (previous[target] === undefined) {
            return null;
        }

        // Retrieve a path from the dictionary of previous nodes and reverse it.
        var reversePath = [];
        var element = target;
        while (element !== undefined) {
            reversePath.push(element);
            element = previous[element];
        }

        return reversePath.reverse();
    }

    return Dijkstra;
})();

var JourneyBase = (function () {

    /**
     * A journey base.
     * @constructor
     * @param {String} graphs A list of graphs.
     * @param {Boolean} usePenalty Value indicating if a penalty should be used.
     */
    function JourneyBase(graphs, usePenalty) {
        this.graphs = graphs;
        this.usePenalty = usePenalty;
        this.started = false;
        this.dijkstra = new Dijkstra();
    }

    // Private function for creating a graph with a penalty for a certain property with
    // a certain value.
    var getPenaltyGraph = function (graph, weightKey, penaltyKey, penalties) {

        var penaltyGraph = { edges: {} };

        for (var k in graph.edges) {
            if (!Object.prototype.hasOwnProperty.call(graph.edges, k)) {
                continue;
            }

            penaltyGraph.edges[k] = {};
            var edges = graph.edges[k];

            for (var m in edges) {
                if (!Object.prototype.hasOwnProperty.call(edges, m)) {
                    continue;
                }

                penaltyGraph.edges[k][m] = {};

                // Add penalty to weight if the value of the penalty key corresponds
                // to the specified penalty value.
                if (edges[m][penaltyKey] in penalties) {
                    penaltyGraph.edges[k][m][weightKey] = edges[m][weightKey] + penalties[edges[m][penaltyKey]];
                }
                else {
                    penaltyGraph.edges[k][m][weightKey] = edges[m][weightKey];
                }
            }
        }

        return penaltyGraph;
    }

     /**
     * Calculate the shortest path between two nodes in a graph.
     * @param {String} from
     * @param {String} to
     * @return {Array} An array of node names corresponding to the path
     */
    JourneyBase.prototype.shortestPath = function (from, to) {
        var index = undefined;
        for (var i = 0; i < this.graphs.length; i++) {
            // Ensure that both nodes exist in the graph.
            if (this.graphs[i].nodes.indexOf(from) > -1 &&
                this.graphs[i].nodes.indexOf(to) > -1) {
                index = i;
                break;
            }
        }

        if (index === undefined) {
            return null;
        }

        var journeyGraph = this.graphs[index];
        if (this.usePenalty === true) {
            journeyGraph =
                getPenaltyGraph(
                    journeyGraph,
                    'weight',
                    'direction',
                    { step_backward: 30, turn_u: 15 });
        }

        var path = this.dijkstra.shortestPath(journeyGraph, from, to, 'weight');

        return { path: path, index: index };
    }

    /**
     * Gets a value indicating whether a journey is ongoing.
     * @return {Boolean} A value indicating whether a journey is ongoing.
     */
    JourneyBase.prototype.isStarted = function () {
        return this.started;
    }

    return JourneyBase;
})();

var Journey = (function () {

    /**
     * A journey.
     * @constructor
     * @param {String} graphs A list of graphs.
     * @param {String} intervalTime The maximum time between navigation.
     * @param {Function} navigationAction The action to execute on navigation.
     * @param {Function} startAction The action to run when starting a journey.
     * @param {Function} stopAction The action to run when stopping a journey.
     * @param {Function} preloadAction The action to run when stopping a journey.
     * @param {Boolean} usePenalty Value indicating if a penalty should be used.
     */
    function Journey(graphs, intervalTime, navigationAction, startAction, stopAction, preloadAction, usePenalty) {

        JourneyBase.apply(this, [graphs, usePenalty]);

        this.intervalTime = intervalTime;
        this.navigationAction = navigationAction;
        this.startAction = startAction;
        this.stopAction = stopAction;
        this.preloadAction = preloadAction;
        this.timeoutToken = undefined;
        this.path = undefined;
        this.graphIndex = undefined;
        this.currentIndex = 0;
    }

    // Inheriting from JourneyBase
    Journey.prototype = Object.create(JourneyBase.prototype);
    Journey.prototype.constructor = Journey;

    // Private function for calculating the interval value.The max distance of an edge is
    // 20. The interval is the fraction of the max distance multiplied by the current
    // interval time. A smallest value is defined to avoid too fast navigation..
    var getInterval = function (edges, node, intervalTime) {
        var distance = edges[node].weight;
        return Math.max((distance / 20) * intervalTime, 0.7 * 1000);
    }

    // Private callback function for setInterval.
    var onNavigation = function (self) {
        var pathLength = self.path.length;
        self.currentIndex++;

        if (self.started !== true || self.currentIndex >= pathLength) {
            self.stop();
            return;
        }

        self.navigationAction(self.path[self.currentIndex]);

        if (self.currentIndex === pathLength - 1) {
            self.stop();
            return;
        }

        if (self.currentIndex + 10 <= pathLength - 1) {
            self.preloadAction([self.path[self.currentIndex + 10]]);
        }

        var currentInterval =
            getInterval(
                self.graphs[self.graphIndex].edges[self.path[self.currentIndex - 1]],
                self.path[self.currentIndex],
                self.intervalTime);

        self.timeoutToken = window.setTimeout(function () { onNavigation(self); }, currentInterval);
    }

    /**
     * Sets the interval time.
     * @param {Integer} intervalTime
     */
    Journey.prototype.updateInterval = function (intervalTime) {
        this.intervalTime = intervalTime;
    }

    /**
     * Starts a journey between two nodes in a graph.
     * @param {Number} from
     * @param {Number} to
     */
    Journey.prototype.start = function (from, to) {
        if (this.started === true) {
            return;
        }

        var result = this.shortestPath(from, to);
        if (result === null || result.path.length <= 1) {
            return;
        }

        this.started = true;
        this.path = result.path;
        this.graphIndex = result.index;
        this.currentIndex = 0;
        this.startAction();
        this.navigationAction(this.path[this.currentIndex])
        this.preloadAction(this.path.slice(1, Math.min(10, this.path.length)))

        var currentInterval =
            getInterval(
                this.graphs[this.graphIndex].edges[this.path[this.currentIndex]],
                this.path[this.currentIndex + 1],
                this.intervalTime);

        var _this = this;
        this.timeoutToken = window.setTimeout(function () { onNavigation(_this); }, currentInterval);
    }

    /**
     * Stops an ongoing journey between two nodes in a graph.
     */
    Journey.prototype.stop = function () {
        if (this.timeoutToken === undefined || this.started === false) {
            return;
        }

        window.clearTimeout(this.timeoutToken);
        this.timeoutToken = undefined;
        this.currentIndex = 0;
        this.path = undefined;
        this.graphIndex = undefined;

        this.stopAction();

        this.started = false;
    }

    return Journey;
})();

LinearCurve = THREE.Curve.create(

	function (points) {

		this.points = (points == undefined) ? [] : points;

	},

	function (t) {

		var points = this.points;
		var point = (points.length - 1) * t;

		var intPoint = Math.floor(point);
		var weight = point - intPoint;

		var point1 = points[intPoint];
		var point2 = points[intPoint > points.length - 2 ? points.length - 1 : intPoint + 1 ];

		var vector = new THREE.Vector3();
		vector.copy(point1).lerp(point2, weight);

		return vector;

	}
);

var JourneyWrapper = (function ($) {

    /**
     * A journey wrapper.
     * The journey wrapper uses global objects declared in the reconstruction script.
     * @constructor
     */
    function JourneyWrapper() {
        this.initialized = false;
        this.journey = undefined;
        this.destination = undefined;
        this.shots = undefined;
        this.line = undefined;
    }

    // Private function for calculating the desired maximum interval.
    var getInterval = function () {
        var interval = undefined;
        if (controls.animationSpeed === 0) {
            interval = 4 * 1000;
        }
        else {
            interval = (4 - 15 * (controls.animationSpeed)) * 1000;
        }

        return interval;
    }

    // Private function for navigation action of journey. Retrieves a camera,
    // creates its image plane and navigates to it.
    var navigation = function (shot_id) {
        var camera = undefined;
        for (var i = 0; i < camera_lines.length; ++i) {
            if (camera_lines[i].shot_id === shot_id) {
                camera = camera_lines[i];
            }
        }

        if (camera === undefined) {
            return;
        }

        setImagePlaneCamera(camera);
        navigateToShot(camera);
    }

    // Private function which retrieves a camera and
    // creates its image plane.
    var setImagePlane = function (shot_id) {
        var camera = undefined;
        for (var i = 0; i < camera_lines.length; ++i) {
            if (camera_lines[i].shot_id === shot_id) {
                camera = camera_lines[i];
            }
        }

        if (camera === undefined) {
            return;
        }

        setImagePlaneCamera(camera);
    }

    // Private function for preloading images.
    var preload = function (shot_ids) {
        for (var i = 0; i < shot_ids.length; i++) {
            var tempImg = new Image();
            tempImg.src = imageURL(shot_ids[i]);
        }
    }

    // Private function for start action of journey.
    var start = function () {
        setMovingMode('walk');
        $('#journeyButton').html('X');
    }

    // Private function for stop action of journey.
    var stop = function () {
        $('#journeyButton').html('Go');
    }

    // Private function converting shot dictionary with rotations and translations
    // values to shot dictionary with optical centers and viewing directions.
    var convertShots = function (shots) {
        var result = {};

        for (var shot_id in shots) {
            if (!Object.prototype.hasOwnProperty.call(shots, shot_id)) {
                continue;
            }

            var oc = opticalCenter(shots[shot_id]);
            var vd = viewingDirection(shots[shot_id]);

            result[shot_id] = { 'oc': oc, 'vd': vd };
        }

        return result;
    }

    // Private function creating a line geometry based on the optical centers
    // of the shots defined in the path.
    var createLineGeometry = function (shots, path) {
        var material = new THREE.LineBasicMaterial({
            color: 0xffff88,
            linewidth: 5
        });

        var geometry = new THREE.Geometry();

        for (var i = 0; i < path.length; i++) {
            var shot_id = path[i];
            var oc = shots[shot_id]['oc'];
            geometry.vertices.push(new THREE.Vector3(oc.x, oc.y, oc.z));
        }

        var line = new THREE.Line(geometry, material);
        var linearCurve = new LinearCurve(geometry.vertices);

        return { 'line': line, 'linearCurve': linearCurve}
    }

    /**
     * Initializes a journey wrapper.
     * @param {shots} Dictionary of shots with rotation and translation arrays.
     */
    JourneyWrapper.prototype.initialize = function (shots) {
        if ('nav' in urlParams && 'dest' in urlParams) {

            if (shots !== undefined) {
                this.shots = convertShots(shots);
            }

            this.destination = urlParams.dest;
            var _this = this;

            $.getJSON(urlParams.nav, function(data) {

                _this.journey =
                    new Journey(
                        data,
                        getInterval(),
                        navigation,
                        start,
                        stop,
                        preload,
                        true);

                _this.initialized = true;
                $('#journeyButton').show();

                if ('img' in urlParams && selectedCamera !== undefined) {
                    _this.toggleJourney();
                }
            });
        }
    }

    /**
     * Shows the shortest path in the scene.
     */
    JourneyWrapper.prototype.showPath = function () {
        if (this.initialized !== true || selectedCamera === undefined || this.shots === undefined){
            return;
        }

        this.hidePath();

        var path = this.journey.shortestPath(selectedCamera.shot_id, this.destination).path;
        var lineGeometry = createLineGeometry(this.shots, path);
        this.line = lineGeometry.line;
        this.line.name = "shortestPath"
        scene.add(this.line);
        render();
    }

    /**
     * Hides the shortest path from the scene.
     */
    JourneyWrapper.prototype.hidePath = function () {
        if (this.initialized !== true || this.line === undefined){
            return;
        }

        if (this.line !== undefined) {
            var sceneLine = scene.getObjectByName(this.line.name);
            scene.remove(sceneLine);
            this.line = undefined;
            render();
        }
    }

    /**
     * Updates the interval.
     */
    JourneyWrapper.prototype.updateInterval = function () {
        if (this.initialized !== true) {
            return;
        }

        this.journey.updateInterval(getInterval());
    }

    JourneyWrapper.prototype.smoothStart = function () {
        if (this.initialized !== true) {
            return;
        }

        var path = this.journey.shortestPath(selectedCamera.shot_id, this.destination).path;

        if (path.length <= 1) {
            return;
        }

        var lineGeometry = createLineGeometry(this.shots, path);
        this.path = path;
        this.linearCurve = lineGeometry.linearCurve;

        var pos = this.linearCurve.getPointAt(0);
        camera.position.copy(pos);

        var shot_id1 = path[0];
        var vd1 = this.shots[shot_id1]['vd'].normalize();

        var lookAt = new THREE.Vector3();
        lookAt.addVectors(pos, vd1);

        camera.lookAt(lookAt);

        controls.adjustAnimationToObject();

        preload(this.path.slice(1, Math.min(10, this.path.length)));
        this.smoothJourneyStarted = true;
        this.startTime = Date.now();
        this.currentIndex = 0;
        setImagePlane(this.path[1]);
    }

    JourneyWrapper.prototype.render = function () {
        if (this.smoothJourneyStarted !== true) {
            return;
        }

        if (this.currentIndex + 10 <= this.path.length - 1) {
            preload([this.path[this.currentIndex + 10]]);
        }

        var path = this.path;
        var linearCurve = this.linearCurve;
        var length = linearCurve.getLength();
        var interval = getInterval();
        var time = Date.now();
        var elapsed = time - this.startTime;

        var totalTime = 2 * interval * length / 20;

        var u = Math.min(elapsed / totalTime, 1);

        var t = linearCurve.getUtoTmapping(u);
        var point = (path.length - 1) * t;

        var intPoint = Math.floor(point);
        var weight = point - intPoint;

        if (intPoint > this.currentIndex && intPoint < this.path.length) {
            this.currentIndex = intPoint;
            setImagePlane(this.path[this.currentIndex + 1]);
        }

        var shot_id1 = path[intPoint];
        var vd1 = this.shots[shot_id1]['vd'].normalize();

        var shot_id2 = path[Math.min(intPoint + 1, this.path.length - 1)];
        var vd2 = this.shots[shot_id2]['vd'].normalize();

        var line3 = new THREE.Line3(vd1, vd2);
        var direction = line3.at(weight).normalize();

        var position = linearCurve.getPointAt(u);

        var lookAt = new THREE.Vector3();
        lookAt.addVectors(position, direction);

        camera.position.copy(position);
        camera.lookAt(lookAt);

        controls.adjustAnimationToObject();

        if (elapsed / totalTime > 1) {
            this.smoothJourneyStarted = false;
        }
    }

    /**
     * Stops a journey.
     */
    JourneyWrapper.prototype.stop = function () {
        if (this.initialized !== true) {
            return;
        }

        if (this.journey.isStarted() === true) {
            this.journey.stop();
        }
    }

    /**
     * Toggles the journey state between started and stopped.
     */
    JourneyWrapper.prototype.toggleJourney = function () {
        if (this.initialized !== true) {
            return;
        }

        if (this.journey.isStarted() === true) {
            this.journey.stop();
            return;
        }

        if (selectedCamera === undefined) {
            return;
        }

        this.journey.updateInterval(getInterval());
        this.journey.start(selectedCamera.shot_id, this.destination);
    }

    return JourneyWrapper;
})(jQuery);

var journeyWrapper = new JourneyWrapper();

