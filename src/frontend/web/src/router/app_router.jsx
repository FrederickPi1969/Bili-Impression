import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import SearchPage from '../components/search_page';
import KnowledgeGraph from '../components/knowledge_graph';
import PopularityVariation from '../components/popularity_variation';
import SexDistribution from '../components/sex_distribution';
import WordCloud from '../components/word_cloud';
import TopUploaders from '../components/top_uploaders';
import AnimatedRouter from 'react-animated-router';
import Visualization from '../components/visualization'
import 'react-animated-router/animate.css';

export default function AppRouter() {
    return (
        <BrowserRouter>
            <div className="container">
                <AnimatedRouter>
                    <Route component={SearchPage} path='/' exact={true} />
                    <Route component={Visualization} path='/visualization' exact={true}/>
                    <Route component={WordCloud} path='/visualization/wordCloud' exact={true}/>
                    <Route component={SexDistribution} path='/visualization/sexDistribution' exact={true}/>
                    <Route component={TopUploaders} path='/visualization/topUploaders' exact={true}/>
                    <Route component={PopularityVariation} path='/visualization/popularityVariation' exact={true}/>
                    <Route component={KnowledgeGraph} path='/visualization/knowledgeGraph' exact={true}/>
                </AnimatedRouter>
            </div>
        </BrowserRouter>
    );
}
