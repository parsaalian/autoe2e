import { createSvgIcon, SvgIconProps } from "@material-ui/core";
import React from "react";

const PermissionGroupsIcon = createSvgIcon(
  <path
    fillRule="evenodd"
    clipRule="evenodd"
    d="M16 4C13.7909 4 12 5.79086 12 8V11.9355C13.205 11.3367 14.5632 11 16 11C17.4368 11 18.795 11.3367 20 11.9355V8C20 5.79086 18.2091 4 16 4ZM22 13.2917V8C22 4.68629 19.3137 2 16 2C12.6863 2 10 4.68629 10 8V13.2917C8.15875 14.9396 7 17.3345 7 20C7 24.9706 11.0294 29 16 29C20.9706 29 25 24.9706 25 20C25 17.3345 23.8412 14.9396 22 13.2917ZM14 18C14 17.4477 14.4477 17 15 17H17C17.5523 17 18 17.4477 18 18C18 18.5523 17.5523 19 17 19V22C17 22.5523 16.5523 23 16 23C15.4477 23 15 22.5523 15 22V19C14.4477 19 14 18.5523 14 18ZM23 20C23 23.866 19.866 27 16 27C12.134 27 9 23.866 9 20C9 16.134 12.134 13 16 13C19.866 13 23 16.134 23 20Z"
    fill="currentColor"
  />,
  "PermissionGroups",
);

export default function PermissionGroups(props: SvgIconProps) {
  return <PermissionGroupsIcon {...props} viewBox="0 0 32 32" />;
}
