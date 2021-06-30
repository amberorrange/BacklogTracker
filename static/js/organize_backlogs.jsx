"use strict";

const BacklogEntry = (props) => {
  return (
    <div className="backlog_entry">
      <h4 className="backlog_title">{props.title}</h4>
      <img  className="backlog_image" src={props.image} /> <br></br>
      Genre: {props.genre} <br></br>
      Ownership Status: {props.ownership_status}<br></br>
      Play Status: {props.play_status ? 'Currently Playing' : 'Not Playing'}<br></br>
      Playing On: {props.platform}<br></br>
    </div>
  );
}

const FilterOption = ({ options, disabledLabel }) => {
  return (
    <React.Fragment>
       <option value="" defaultValue disabled>
        {disabledLabel}
      </option>
      <option value="All" key="All">All</option>
      {options.map((option) => (
        <option key={option} value={option}>{option}</option> 
      ))}
    </React.Fragment>
  )
}

const Select = (props) => {
  return (
    <div>
      <select value={props.value} onChange={props.onchange}>
        <FilterOption
          disabledLabel=""
          options={props.options}
        />
      </select>
    </div>
  )
}

const FilterOptions = (props) => {
  return (
    <div> 
      <Select 
        value={props.value}
        onchange={props.onchange}
        options={props.options}
      />
  </div>
  )
}


const BacklogContainer = () => {
  const [backlogs, updateBacklogs] = React.useState([]);
  const [displayedBacklogs, updateDisplayedBacklogs] = React.useState([]);
  const [genreFilter, updateGenreFilter] = React.useState(""); 
  const [genresList, updateGenresList] = React.useState([])
  const [platformFilter, updatePlatformFilter] = React.useState("")
  const [platformsList, updatePlatformsList] = React.useState([])
  const [ownershipFilter, updateOwnershipFilter] = React.useState("")
  const [ownershipList, updateOwnershipList] = React.useState([])
  const [playstatusFilter, updatePlaystatusFilter] = React.useState("")
  const [playstatusList, updatePlaystatusList] = React.useState([])
  const [sortingChoice, updateSortingChoice] = React.useState("")
  const [sortingList, updateSortingList] = React.useState([])


  React.useEffect(() => {
    fetch("/api/backlog")
      .then((response) => response.json())
      .then((data) => {console.log(data); return data})
      .then((data) => {
        // Load initial backlog data into component
        updateBacklogs(data);
        updateDisplayedBacklogs(data);
      });
  }, []);



  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.platform)
    updatedList = new Set(updatedList)
    updatePlatformsList([...updatedList, ...platformsList])
  }, [backlogs])

  React.useEffect(() => {
    if (platformFilter === "All") {
      updateDisplayedBacklogs(backlogs)
    } else {
      let updatedDisplay = backlogs.filter((backlog) => backlog.platform === platformFilter)
      updateDisplayedBacklogs(updatedDisplay)
    }
  }, [platformFilter])




  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.play_status ? 'Currently Playing' : 'Not Playing')
    updatedList = new Set(updatedList)
    updatePlaystatusList([...updatedList, ...playstatusList])
  }, [backlogs])
  
  React.useEffect(() => {
    if (playstatusFilter === 'Currently Playing') {
      updateDisplayedBacklogs(backlogs.filter((backlog) => {
        return backlog.play_status === true;
      }));
    } else if (playstatusFilter === 'Not Playing') {
      updateDisplayedBacklogs(
        backlogs.filter((backlog) => backlog.play_status === false)
      );
    } else {
      updateDisplayedBacklogs(backlogs)
    }
  }, [playstatusFilter])




  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.ownership_status)
    updatedList = new Set(updatedList)
    updateOwnershipList([...updatedList, ...ownershipList])
  }, [backlogs])

  React.useEffect(() => {
    if (ownershipFilter === "All") {
      updateDisplayedBacklogs(backlogs)
    } else {
      let updatedDisplay = backlogs.filter((backlog) => backlog.ownership_status === ownershipFilter)
      updateDisplayedBacklogs(updatedDisplay)
    }
  }, [ownershipFilter])

  

  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.genre)
    updatedList = new Set(updatedList)
    updateGenresList([...updatedList, ...genresList])
  }, [backlogs])

  React.useEffect(() => {
    if (genreFilter === "All") {
      updateDisplayedBacklogs(backlogs)
    } else {
      let updatedDisplay = backlogs.filter((backlog) => backlog.genre === genreFilter)
      updateDisplayedBacklogs(updatedDisplay)
    }
  }, [genreFilter])



  

  React.useEffect(() => {
    updateSortingList(['Genre', 'Platform', 'Ownership Status', 'Play Status'])
  }, [backlogs])


  React.useEffect(() => {
    // let choice = '';

    // if (sortingChoice === 'Genre') {
    //   choice = 'genre'
    // } else if (sortingChoice === 'Platform') {
    //   choice = 'platform'
    // } else if (sortingChoice === 'Play Status') {
    //   choice = 'play_status'
    // } else if (sortingChoice === 'Ownership Status') {
    //   choice = 'ownership_status'
    // } else {
    //   choice = 'All'
    // } 
    
    // console.log(sortingChoice, 'SORTING CHOICE')
    // console.log(choice, 'CHOICE')

    if (sortingChoice === "All") {
      updateDisplayedBacklogs(backlogs)
    } else {
      const updatedBacklogs = backlogs.sort((backlog1, backlog2) => {
        if (backlog1[sortingChoice] > backlog2[sortingChoice]) {
          return 1;
        } else if ((backlog1[sortingChoice] < backlog2[sortingChoice])) {
          return -1;
        } else {
          return 0;
        }
      });
      updateDisplayedBacklogs(updatedBacklogs)
      console.log(updatedBacklogs, ' UPDATED DISPLAY THAT SHOULD BE SHOWING')
    }
  }, [sortingChoice])



  const handleSortSelect = (e) => {
    updateSortingChoice(e.target.value)
  }

  const handleSelect = (e) => {
    updateGenreFilter(e.target.value)
  }

  const handleplatformSelect = (e) => {
    updatePlatformFilter(e.target.value)
  }

  const handleOwnershipSelect = (e) => {
    updateOwnershipFilter(e.target.value)
  }

  const handlePlaystatusSelect = (e) => {
    updatePlaystatusFilter(e.target.value)
  }


  const backlogEntries = [];
  for (const backlog of displayedBacklogs) {
    backlogEntries.push(
      <BacklogEntry
        key={backlog.backlog_id}
        title={backlog.game.title}
        image= {backlog.game.image}
        genre= {backlog.genre}
        ownership_status= {backlog.ownership_status}
        play_status={backlog.play_status}
        platform={backlog.platform}
      />
    );
  }

  return (
    <div>
      {backlogEntries} <br></br>
      
      Genres:
      <FilterOptions 
        value={genreFilter}
        onchange={handleSelect}
        options={genresList}
      />
      
      <br></br>
      Platforms:
      <FilterOptions 
        value={platformFilter}
        onchange={handleplatformSelect}
        options={platformsList}
      />


      <br></br>
      Ownership Status:
      <FilterOptions 
        value={ownershipFilter}
        onchange={handleOwnershipSelect}
        options={ownershipList}
      />


      <br></br>
      Play Status:
      <FilterOptions 
        value={playstatusFilter}
        onchange={handlePlaystatusSelect}
        options={playstatusList}
      />


      <br></br>
      Sort By:
      <FilterOptions
        value={sortingChoice}
        onchange={handleSortSelect}
        options={sortingList}
      />
    </div>
  )
};


ReactDOM.render(<BacklogContainer />, document.getElementById("container"));