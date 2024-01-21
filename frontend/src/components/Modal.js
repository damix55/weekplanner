import React from 'react';
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Input,
  Label,
  FormFeedback,
} from 'reactstrap';
import DayPickerInput from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';


function ModalComponent({activeItem, repeatItem, toggle, handleSubmit, handleChange, handleDayChange, errors, handleDelete, repeat, handleRepeat, handleUntilChange, handleEvery}) {

  const convertStingToDate = (day) => {
    var parts = day.split('-');
    var date = new Date(parts[0], parts[1] - 1, parts[2]); 
    return date
  }

  const getNextDay = (day) => {
    day.setDate(day.getDate() + 1);
    return day
  }
  
  return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}> Task Item</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="task-title">Title</Label>
              <Input
                invalid={errors !== undefined && errors.title}
                type="text"
                id="task-title"
                name="title"
                value={activeItem.title}
                onChange={handleChange}
                placeholder="Enter Task Title"
              />
              <FormFeedback>
                { errors !== undefined ? errors.title : '' }
              </FormFeedback>
            </FormGroup>
            <FormGroup>
              <Label for="task-description">Description</Label>
              <Input
                invalid={errors !== undefined && errors.description}
                type="text"
                id="task-description"
                name="description"
                value={activeItem.description}
                onChange={handleChange}
                placeholder="Enter Task description"
              />
              <FormFeedback>
                { errors !== undefined ? errors.description : '' }
              </FormFeedback>
            </FormGroup>
            <FormGroup>
              <Label for="task-priority">Priority</Label>
              <Input
                type="select"
                name="priority"
                id="task-priority"
                value={activeItem.priority}
                onChange={handleChange}
              >
                <option value="0">None</option>
                <option value="1">Low</option>
                <option value="2">Medium</option>
                <option value="3">High</option>
              </Input>
            </FormGroup>
            <FormGroup>
              <Label for="task-date">Date</Label>
              <br></br>
              <DayPickerInput
                onDayChange={handleDayChange}
                id="task-date"
                name="date"
                value={activeItem.date}
                inputProps={{
                  className: errors !== undefined && errors.date ? 'is-invalid form-control' : 'form-control',
                  name: 'date',
                }}
                style={{width: 100 + '%'}}
                dayPickerProps={{
                  modifiers: { disabled: [ { before: new Date() } ] }
                }}
                placeholder="YYYY-MM-DD"
              />
              { errors !== undefined && errors.date ? <div class="invalid-feedback" style={{display: 'block'}}> {errors.date} </div> : '' }
            </FormGroup>
            { activeItem.date ? 
            <FormGroup check>
              <Label check>
                <Input
                  type="checkbox"
                  name="repeat"
                  checked={repeat}
                  onChange={handleRepeat}
                />
                Repeat task
              </Label>
            </FormGroup>
            : '' }
          </Form>
            { repeat && activeItem.date ? 
              <Form>
              <FormGroup>
                <Label for="task-date">Until</Label>
                <br></br>
                <DayPickerInput
                  onDayChange={handleUntilChange}
                  id="task-until"
                  name="until"
                  value={repeatItem.until}
                  inputProps={{
                    className: errors !== undefined && errors.until ? 'is-invalid form-control' : 'form-control',
                    name: 'until',
                  }}
                  style={{width: 100 + '%'}}
                  dayPickerProps={{
                    modifiers: { disabled: [ { before: getNextDay(convertStingToDate(activeItem.date)) } ] }
                  }}
                  placeholder="YYYY-MM-DD"
                />
                { errors !== undefined && errors.until ? <div class="invalid-feedback" style={{display: 'block'}}> {errors.until} </div> : '' }
              </FormGroup>
              <FormGroup>
                <Label for="task-every">Every (days)</Label>
                <Input
                  invalid={errors !== undefined && errors.every}
                  type="every"
                  id="task-every"
                  name="every"
                  value={repeatItem.every}
                  onChange={handleEvery}
                  placeholder="1"
                />
                <FormFeedback>
                  { errors !== undefined ? errors.every : '' }
                </FormFeedback>
              </FormGroup> 
              </Form>
            : ''}
        </ModalBody>
        <ModalFooter>
          <Button
            id="save-button"
            color="success" 
            onClick={() => handleSubmit(activeItem, repeatItem)}>
            Save
          </Button>
        {activeItem.id ? (
          <Button
            id="delete-button"
            color="danger"
            onClick={() => handleDelete(activeItem)}>
            Delete
          </Button>
          ) : ('')}
        </ModalFooter>
      </Modal>

  )
}

export default ModalComponent
