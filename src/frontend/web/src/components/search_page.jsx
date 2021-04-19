import React, { useState } from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles'
import InputLabel from '@material-ui/core/InputLabel'
import MenuItem from '@material-ui/core/MenuItem'
import FormControl from '@material-ui/core/FormControl'
import Select from '@material-ui/core/Select'
import InputBase from '@material-ui/core/InputBase'
import { Link } from 'react-router-dom'
import "bootstrap/dist/css/bootstrap.css";

const BootstrapInput = withStyles((theme) => ({
    root: {
      	'label + &': {
        	marginTop: theme.spacing(3),
      	},
    },
    input: {
		fontSize: 16,
		position: 'relative',
		borderRadius: 8,
		border: '1px solid #ced4da',
		backgroundColor: theme.palette.background.paper,
		padding: '10px 26px 10px 12px',
		transition: theme.transitions.create(['border-color', 'box-shadow']),
		fontFamily: [
			'-apple-system',
			'Arial',
      	].join(','),
      	'&:focus': {
			borderRadius: 8,
			borderColor: '#80bdff',
			boxShadow: '0 0 0 0.2rem rgba(0,123,255,.25)',
      	},
    },
}))(InputBase);
  
const useStyles = makeStyles((theme) => ({
	keyword: {
		margin: theme.spacing(1),
		width: '60%',
		left: '6%',
		marginTop:'10%'
	},
    margin: {
        margin: theme.spacing(1),
		left: '6%',
		width: '12%',
		marginTop:'10%'
    },
	box: {
		margin: theme.spacing(1),
		width: '200px',
		left: '12%',
	},
	start: {
		margin: theme.spacing(1),
		marginTop: '2%',
		width: '200px',
		left: '25%',
	}
}));

export default function SearchPage() {
	const [options, setOptions] = useState({
		keyword: '',
		maxPage: 1,
		maxCandidate: 20,
		rankMethod: '0',
		subArea: '0'
	});
	const classes = useStyles()
	const inputUpdate = event => {
		const { id, value } = event.target;
		setOptions(prevState => ({
			...prevState,
			[id]: value
		}));
	};
	const rankMethodUpdate = event => {
		const { value } = event.target;
		setOptions(prevState => ({
			...prevState,
			['rankMethod']: value
		}));
	};
	const subAreaUpdate = event => {
		const { value } = event.target;
		setOptions(prevState => ({
			...prevState,
			['subArea']: value
		}));
	};
	return (
		<div>
			<div>
				<label style={{fontSize: 72, color: '#FFB6C1', marginTop: '20%', marginLeft: 320}}>
					Bili-Impression
				</label>
			</div>
			<div>
				<FormControl className={classes.keyword}>
					<InputLabel htmlFor="keyword-box">keyword</InputLabel>
					<BootstrapInput 
						id='keyword' 
						// value={keyword} 
						onChange={inputUpdate}
					/>
				</FormControl>
				<FormControl className={classes.margin}>
					<InputLabel htmlFor="maxPage-box">maxPage</InputLabel>
					<BootstrapInput 
						id='maxPage' 
						// value={maxPage} 
						onChange={inputUpdate}
					/>
				</FormControl>
				<FormControl className={classes.margin}>
					<InputLabel htmlFor="maxCandidate-box">maxCandidate</InputLabel>
					<BootstrapInput 
						id='maxCandidate' 
						// value={maxCandidate} 
						onChange={inputUpdate}
					/>
				</FormControl>
			</div>
			<div>
				<FormControl className={classes.box}>
					<InputLabel id='select-subArea-box'>SubArea</InputLabel>
					<Select 
						labelId='select-subArea-box'
						id='subArea'
						// value={subArea}
						onChange={subAreaUpdate}
					>
						<MenuItem value={"0"}>All Subarea</MenuItem>
						<MenuItem value={"1"}>Animation</MenuItem>
						<MenuItem value={"2"}>Bangumi</MenuItem>
						<MenuItem value={"3"}>Domestic</MenuItem>
						<MenuItem value={"4"}>Music</MenuItem>
						<MenuItem value={"5"}>Dance</MenuItem>
						<MenuItem value={"6"}>Game</MenuItem>
						<MenuItem value={"7"}>Knowledge</MenuItem>
						<MenuItem value={"8"}>Digital Tech</MenuItem>
						<MenuItem value={"9"}>Lifestyle</MenuItem>
						<MenuItem value={"10"}>Food</MenuItem>
						<MenuItem value={"11"}>Autotune Remix</MenuItem>
						<MenuItem value={"12"}>Fashion</MenuItem>
						<MenuItem value={"13"}>News</MenuItem>
						<MenuItem value={"14"}>Entertainment</MenuItem>
						<MenuItem value={"15"}>Television</MenuItem>
						<MenuItem value={"16"}>Documentary</MenuItem>
						<MenuItem value={"17"}>Film and Movie</MenuItem>
						<MenuItem value={"18"}>TV Series</MenuItem>
					</Select>
				</FormControl>
				<FormControl className={classes.box}>
					<InputLabel id='select-rank-box'>RankMethod</InputLabel>
					<Select 
						labelId='select-rank-box'
						id='rankMethod'
						// value={rankMethod}
						onChange={rankMethodUpdate}
					>
						<MenuItem value={"0"}>Comprehensive Rank</MenuItem>
						<MenuItem value={"1"}>Most Click</MenuItem>
						<MenuItem value={"3"}>Most Danmaku</MenuItem>
					</Select>
				</FormControl>
				<FormControl className={classes.start}>
					<Link 
						className='btn btn-primary'
						to={{
							pathname: '/visualization',
							options
						}}
					>
						Generate!
					</Link>
				</FormControl>
			</div>
			{/* <div style={{marginLeft: '15%', marginTop:'15%'}}>
				<Link
					className='btn btn-primary'
					to={{
						pathname: '/visualization/wordCloud',
						options
					}}
					style={{marginRight: 15}}
				>
					WordCloud
				</Link>
				<Link
					className='btn btn-primary'
					to={{
						pathname: '/visualization/sexDistribution',
						options
					}}
					style={{marginRight: 15}}
				>
					SexDistribution
				</Link>
				<Link
					className='btn btn-primary'
					to={{
						pathname: '/visualization/topUploaders',
						options
					}}
					style={{marginRight: 15}}
				>
					Top Uploaders
				</Link>
				<Link
					className='btn btn-primary'
					to={{
						pathname: '/visualization/popularityVariation',
						options
					}}
					style={{marginRight: 15}}
				>
					Popularity Variation
				</Link>
				<Link
					className='btn btn-primary'
					to={{
						pathname: '/visualization/knowledgeGraph',
						options
					}}
					style={{marginRight: 15}}
				>
					Knowledge Graph
				</Link>
			</div> */}
		</div>
	)
}