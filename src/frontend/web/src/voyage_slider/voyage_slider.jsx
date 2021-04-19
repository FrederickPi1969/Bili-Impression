import React, { Component } from "react";
import Carousel from "react-spring-3d-carousel";
import { v4 as uuid } from "uuid";
import { config } from "react-spring";
import icon from './word_cloud.png'
import { Link } from 'react-router-dom'

let options = {};

function get_content() {
  return (
    <Link
      to={{
        pathname: '/visualization/wordCloud',
        options
      }}
      style={{ marginLeft: 48 }}
    >
      <img src={icon} alt="1" width="80%" />
    </Link>
  )
}

export default class VoyageSlider extends Component {
  constructor(props) {
    super(props);
    options = props.data.options
  };
  state = {
    goToSlide: 0,
    offsetRadius: 2,
    showNavigation: true,
    config: config.wobbly,
  };
  slides = [
    {
      key: uuid(),
      content: get_content()
    },
    {
      key: uuid(),
      content: get_content()
    },
    {
      key: uuid(),
      content: get_content()
    },
    {
      key: uuid(),
      content: get_content()
    },
    {
      key: uuid(),
      content: get_content()
    }
  ].map((slide, index) => {
    return {
      ...slide, onClick: () => {
        switch (index) {
          case 0:
            console.log("slide #%s", index.toString());
            this.setState({ icon1: "100%" });
            break;
          case 1:
            console.log("slide #%s", index.toString());
            this.setState({ icon2: "100%" });
            break;
          case 2:
            console.log("slide #%s", index.toString());
            this.setState({ icon3: "100%" });
            break;
          case 3:
            console.log("slide #%s", index.toString());
            this.setState({ icon4: "100%" });
            break;
          case 4:
            console.log("slide #%s", index.toString());
            this.setState({ icon5: "100%" });
            break;
        }
        this.setState({ goToSlide: index })
      }
    };
  });


  render() {
    return (
      <div style={{ width: "80%", height: "600px", margin: "0 auto" }}>
        <Carousel
          slides={this.slides}
          goToSlide={this.state.goToSlide}
          offsetRadius={this.state.offsetRadius}
          showNavigation={this.state.showNavigation}
          animationConfig={this.state.config}
        />
      </div>
    );
  };
};

