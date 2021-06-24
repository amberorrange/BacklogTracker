"use strict";

function BacklogEntry(props) {
  return (
    <div className="backlog_entry">
      {props.title} <br></br>
      <img  className="backlog_image" src={props.image} /> <br></br>
      Genre: {props.genre} <br></br>
      Ownership Status: {props.ownership_status}<br></br>
      Play Status: {props.play_status ? 'Currently playing' : 'Not playing'}<br></br>
      Playing On: {props.platform}<br></br>
    </div>
  );
}

function filterOption(props) {
  return (
    <option value="{props.name}">{props.name}</option>
  )

}

function BacklogContainer() {
  const [backlogs, updateBacklogs] = React.useState([]);
  const [displayedBacklogs, updateDisplayedBacklogs] = React.useState([]);
  const [genreFilter, updateGenreFilter] = React.useState(undefined); // ex.: 'fantasy', 'RPG'

  React.useEffect(() => {
    fetch("/api/backlog")
      .then((response) => response.json())
      .then((data) => {
        // Load initial backlog data into component
        updateBacklogs(data);
        updateDisplayedBacklogs(data);
      });
  }, []);

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

  const genres = [];
  for (const backlog of backlogs) {
    <filterOption
      key={backlog.genre}
      name={backlog.genre}
      />
  } 


  return <div>{backlogEntries}  </div>;
}

ReactDOM.render(<BacklogContainer />, document.getElementById("container"));
















