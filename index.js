import Vue from 'vue'
import VueRouter from 'vue-router'
import Buefy from 'buefy'
import VueClipboard from 'vue-clipboard2'
import 'buefy/lib/buefy.css'
import 'font-awesome/css/font-awesome.css'

import CopiableText from './components/CopiableText'
import Username from './components/Username'
import Nodename from './components/Nodename'
import NodesTable from './components/NodesTable'

import App from './App'
import Home from './pages/Home'
import Datacenters from './pages/Datacenters'
import Datacenter from './pages/Datacenter'
import Nodes from './pages/Nodes'
import Node from './pages/Node'
import Projects from './pages/Projects'
import Project from './pages/Project'

Vue.use(VueRouter)
Vue.use(Buefy)
Vue.use(VueClipboard)

Vue.component('copy', CopiableText)
Vue.component('username', Username)
Vue.component('nodename', Nodename)
Vue.component('nodestable', NodesTable)

const router = new VueRouter({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/datacenters',
            name: 'datacenters',
            component: Datacenters
        },
        {
            path: '/datacenters/:id',
            name: 'datacenter',
            component: Datacenter
        },
        {
            path: '/nodes',
            name: 'nodes',
            component: Nodes
        },
        {
            path: '/nodes/:id',
            name: 'node',
            component: Node
        },
        {
            path: '/projects',
            name: 'projects',
            component: Projects
        },
        {
            path: '/projects/:id',
            name: 'project',
            component: Project
        }
    ]
})

const app = new Vue({
    router,
    render: h => h(App)
}).$mount('#app');