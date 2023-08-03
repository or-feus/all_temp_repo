import React, {SyntheticEvent, useState} from "react";
import {FieldError, FieldErrors, useForm} from "react-hook-form";
import {isReadonlyAssignmentDeclaration} from "tsutils";

interface LoginForm {
  username: string
  password: string
  email: string
}


export default function Forms() {

  const {register, handleSubmit, formState: {errors}} = useForm<LoginForm>({
    mode: "onBlur"
  })
  const onValid = (data: LoginForm) => {
    console.log("im valid")
  }

  const onInvalid = (error: FieldErrors) => {
    console.log(error)
  }

  return (
    <form onSubmit={handleSubmit(onValid, onInvalid)}>
      <input
        {...register("username", {
          required : "Username is required",
          minLength: {
            message: "The username should be longer than 5 chars.",
            value  : 5,
          }
        })}
        type="text"
        placeholder="Username"/>
      <input
        {...register("email", {
          required: "Email is required",
          validate: {
            notGmail: (value) => !value.includes("@gmail.com") ? "" : "Gmail is not allowed"
          }
        })}
        type="email"
        placeholder="Email"/>
      {errors.email?.message}
      <input
        {...register("password", {
          required: "Password is required"
        })}
        type="password"
        placeholder="Password"/>
      <input
        type="submit"
        value="Create Account"/>
    </form>
  )
};