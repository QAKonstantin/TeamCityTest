BASE_URL = "http://localhost:4444/wd/hub"
JETBRAINS_URL = "https://www.jetbrains.com"

# Ссылки для перехода по разделам проекта
CREATE_NEW_PROJECT = ('/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu'
                      '&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects')
EDIT_PROJECT = "/admin/editProject.html?projectId={project_id}"
EDIT_PROJECT_ROOT = "/admin/editProject.html?projectId=_Root"
CREATE_BUILD_CONF = ('/admin/createObjectMenu.html?projectId={project_id}&showMode=createBuildTypeMenu&'
                     'cameFromUrl=%2Fadmin%2FeditProject.html%3FprojectId%3D{project_id}')
EDIT_VCS_ROOT = ('/admin/editVcsRoot.html?action=addVcsRoot&editingScope=buildType%3A{build_conf_id}'
                 '&cameFromUrl=%2Fadmin%2FeditBuildTypeVcsRoots.html%3Finit%3D1%26id%3DbuildType%3A{build_conf_id}'
                 '%26cameFromUrl%3D%252Fadmin%252FeditProject.html%253Finit%253D1%2526projectId%253D{project_id}'
                 '&cameFromTitle=Version%20Control%20Settings&showSkip=true')
EDIT_BUILD_CONF_VCS_ROOT = ('/admin/editBuildTypeVcsRoots.html?init=1&id=buildType:{build_conf_id}'
                            '&cameFromUrl=%2Fadmin%2FeditProject.html%3Finit%3D1%26projectId%3D{project_id}')
NEW_BUILD_STEP_COMMAND_LINE = ('/admin/editRunType.html?id=buildType:{build_conf_id}&runnerId=__NEW_RUNNER__&'
                               'cameFromUrl=%2Fadmin%2FeditBuildRunners.html'
                               '%3Fid%3DbuildType%253A{build_conf_id}%26init%3D1&cameFromTitle=')
EDIT_BUILD_RUNNERS = ('/admin/editBuildRunners.html?id=buildType:{build_conf_id}')
BUILD_CONF_PAGE = ('/buildConfiguration/{build_conf_id}#all-projects')
GENERAL_SETTING_EDIT_BUILD = ("/admin/editBuild.html?id=buildType:{build_conf_id}")
BUILD_CONF_AFTER_REMOVED = ('/admin/editProject.html?projectId={project_id}#buildTypeRemoved')
