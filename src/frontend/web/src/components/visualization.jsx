import React from 'react';
import VoyageSlider from '../voyage_slider/voyage_slider'

const Visualization = props => (
    <div>
        <VoyageSlider data={props.location}/>
    </div>
);

export default Visualization;