# main

## Présentation



## Utilisation

## Détail du contenu



### Classe Interface :

Déclaration :

	class Interface(ct.CTk):

Description :

#### **Methode __init__ :**

Déclaration :

	    def __init__(self) -> None:

#### **Methode createInterface :**

Déclaration :

	    def createInterface(self) -> None:

Description :

	        createInterface
        Fonction de création du corps de l'interface

#### **Methode configActionBt :**

Déclaration :

	    def configActionBt(self) -> None:

Description :

	        configActionBt 
        fonction de modification de l'état des boutons de suppression et de sauvegarde des widgets 

#### **Methode sideWidgetsUptdating :**

Déclaration :

	    def sideWidgetsUptdating(self) -> None:

Description :

	        sideWidgetsUptdating
        Fonction de création des boutons pour les widgets, sur le coté droit de la fenêtre

#### **Methode frame_command :**

Déclaration :

	        def frame_command(w_id):

#### **Methode widgetParametersFrame :**

Déclaration :

	    def widgetParametersFrame(self, widget : str = None)  -> None:

Description :

	        widgetParametersFrame 
        fonction de création de la frame de paramètres du widget

        Parameters
        ----------
        widget : str
            widget dont la fonction doit afficher les paramètres, et leur valeurs respectives

#### **Methode updateCodeFrame :**

Déclaration :

	    def updateCodeFrame(self):

#### **Methode showFontFrame :**

Déclaration :

	    def showFontFrame(self):

Description :

	        showFontFrame 
        Crée la boite "font" dans les paramètres du widget, 
        est appelée lorsque le paramètre font est activé

#### **Methode showLayoutFrame :**

Déclaration :

	    def showLayoutFrame(self, value : str) -> None:

Description :

	        showLayoutFrame 
        crée l'encadré pour les paramètre de layout

        Parameters
        ----------
        value : str
            prend pour valeur le type de layout choisit ( pack ou grid )

#### **Methode search :**

Déclaration :

	    def search(self, dico : dict, target : str):

#### **Methode clear :**

Déclaration :

	    def clear(self, mod : str) -> None:

Description :

	        clear 
        fonction de destruction de widgets

        Parameters
        ----------
        mod : str
            défini les widgets à détruire :
            -all : détruit tous les widgets de l'interface ( frames comprises )
            -itemFrame : détruit les boutons associés aux widgets
            -sets : détruit les labels et entrées de paramètres d'un widget
            -fontframe : détruit la frame des paramètres de font
            -layoutframe : détruit la frame contenant les paramètres de layout du widget

#### **Methode modifyWid :**

Déclaration :

	    def modifyWid(self, *event) -> None:

Description :

	        modifyWid 
        fonction de modification des paramètres d'un widget,
        appele la fonction de chargement/envoi de données (fLoadFunct)

#### **Methode getSettings :**

Déclaration :

	    def getSettings(self, *event) -> None:

Description :

	        getSettings 
        fonction de récupération des paramètres de l'application,
        attribue les paramètres chargé aux variable de l'application

#### **Methode getGeometry :**

Déclaration :

	            def getGeometry():

#### **Methode resetAttr :**

Déclaration :

	    def resetAttr(self) -> None:

Description :

	        resetAttr 
        Fonction de réinitialisation de certaines variables de l'application,
        utilisé lorsque l'application est lancé sans projet ouvert

#### **Methode delWid :**

Déclaration :

	    def delWid(self, *event) -> None:

Description :

	        delWid 
        Fonction de suppression d'un widget.

#### **Methode on_quit :**

Déclaration :

	    def on_quit(self) -> None:

Description :

	        on_quit 
        Détruit la fenêtre lorsque le bouton "Quitter" du menu est pressé

#### **Methode copyCode :**

Déclaration :

	    def copyCode(self, event = None):

#### **Methode configCopy :**

Déclaration :

	    def configCopy(self, *event):

#### **Methode configPaste :**

Déclaration :

	    def configPaste(self, *event):

#### **Methode openPreview :**

Déclaration :

	    def openPreview(self, event = None):

#### **Methode savefile :**

Déclaration :

	    def savefile(self, event = None):

#### **Methode winState :**

Déclaration :

	    def winState(self, event):

#### **Methode use_pack :**

Déclaration :

	    def use_pack(self, *event):

#### **Methode use_grid :**

Déclaration :

	    def use_grid(self,*event):

#### **Methode setBind :**

Déclaration :

	    def setBind(self):

#### **Methode undo :**

Déclaration :

	    def undo(self, *event):

#### **Methode redo :**

Déclaration :

	    def redo(self, *event):

#### **Methode colorPick :**

Déclaration :

	    def colorPick(self,var, param, entry):

#### **Methode delFromCode :**

Déclaration :

	    def delFromCode(self, *event):

#### **Methode openTextTopLevel :**

Déclaration :

	    def openTextTopLevel(self):

#### **Methode openValuesTopLevel :**

Déclaration :

	    def openValuesTopLevel(self):

#### **Methode openCommandTopLevel :**

Déclaration :

	    def openCommandTopLevel(self):

#### **Methode openVariableTopLevel :**

Déclaration :

	    def openVariableTopLevel(self, var):

#### **Methode openProjectApp :**

Déclaration :

	    def openProjectApp(self, *event, **kwargs ) -> None:

Description :

	        openProjectApp 
        Fonction d'ouverture de la fenêtre de projets,
        modifie le nom de l'application si un projet est ouvert

#### **Methode openParameters :**

Déclaration :

	    def openParameters(self, *event) -> None:

Description :

	        openParameters 
        fonction d'ouverture des paramètres, 
        appele la fonction "getSettings" à l'issue

#### **Methode widgetAdding :**

Déclaration :

	    def widgetAdding(self, *event) -> None:

Description :

	        widgetAdding 
        Fonction d'ouverture de la fenêtre d'ajout de Widgets

### Classe StartNotifInterface :

Déclaration :

	class StartNotifInterface(ct.CTk):

Description :

#### **Methode __init__ :**

Déclaration :

	    def __init__(self):

#### **Methode quit :**

Déclaration :

	    def quit(self):

#### **Methode agree :**

Déclaration :

	    def agree(self, arg):
